"""Bounded OpenAI-only triage; mock transport and source-free payload are defaults."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

from .redact import sanitize, Refused
from .validate import validate, SCHEMA, OPERATIONS

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'gpt-6-luna'
ENDPOINT = 'https://api.openai.com/v1/responses'
INPUT_RATE = 0.10 / 1000000
OUTPUT_RATE = 0.50 / 1000000
MAX_OUTPUT = 2048


def safeguard_digest():
    return hashlib.sha256(b''.join((ROOT / name).read_bytes() for name in [
        'triage/redact.py', 'triage/client.py', 'triage/validate.py', 'triage/normalize.py', 'prompts/triage-system.txt'])).hexdigest()


def verified_catalog():
    # Build independently from hash-bound scanner reports, never from a proposed
    # API record's free-text/version fields.
    from .normalize import discover, adapt, bound_report
    entries = discover(ROOT / 'reports/private')
    # The historical baseline is optional in a fresh reproduction. Current
    # pipeline evidence remains mandatory through discover().
    baseline_pointer = ROOT / 'reports/private/day4/latest-manifest.txt'
    if baseline_pointer.is_file():
        manifest_path = Path(baseline_pointer.read_text().strip())
        manifest = json.loads(manifest_path.read_text())
        baseline = next(s for s in manifest['stages'] if s['stage'] == 'iac-baseline')
        entries.append(('iac', bound_report(manifest_path, baseline), {}))
    catalog = {}
    for stage, path, metadata in entries:
        for rule, severity, component, version, location, line, fixed in adapt(stage, json.loads(path.read_text())):
            values = catalog.setdefault(rule, {'versions': set(), 'fixed_versions': set()})
            if version:values['versions'].add(version)
            values['fixed_versions'].update(fixed)
    return catalog


class TransportError(ValueError):
    pass


class MockTransport:
    def __init__(self):
        self.bodies = []

    def __call__(self, body):
        self.last_request_sha256 = hashlib.sha256(body).hexdigest()
        self.bodies.append(body)
        request = json.loads(body)
        payload = json.loads(request['input'])
        result = {'triage': []}
        for finding in payload['findings']:
            severity = finding['severity']
            result['triage'].append({'finding_id': finding['finding_id'], 'issue_id': finding['issue_id'],
                'priority': 'P1' if severity in {'HIGH', 'CRITICAL'} else 'P2' if severity in {'MEDIUM', 'UNKNOWN'} else 'P3',
                'reason': 'Mock policy-based priority; not an independent model result.',
                'fix': ['Review the verified rule and its local evidence.', 'Apply a bounded compatible fix in the owned lab.', 'Rerun the scanner and functional checks; retain remaining risks.'],
                'references': [finding['rule_id']], 'operation': OPERATIONS.get(finding['rule_id'], 'manual-review')})
        return {'model': MODEL, 'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': json.dumps(result)}]}], 'usage': {}}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class OpenAITransport:
    def __init__(self, credential_file, ledger_file, max_spend=1.0, max_requests=3):
        self.credential_file = Path(credential_file)
        self.ledger_file = Path(ledger_file)
        if not 0 < max_spend <= 1 or not 1 <= max_requests <= 3:
            raise TransportError('invalid-pilot-budget')
        self.max_spend = max_spend
        self.max_requests = max_requests

    def __call__(self, body):
        self.last_request_sha256 = hashlib.sha256(body).hexdigest()
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        # UTF-8 bytes plus a fixed overhead conservatively bound text tokens.
        reserve = (len(body) + 2048) * INPUT_RATE + MAX_OUTPUT * OUTPUT_RATE
        with self.ledger_file.open('a+') as ledger:
            fcntl.flock(ledger, fcntl.LOCK_EX)
            ledger.seek(0)
            previous = [json.loads(line) for line in ledger if line.strip()]
            if len(previous) >= self.max_requests or sum(p['reserved_usd'] for p in previous) + reserve > self.max_spend:
                raise TransportError('pilot-budget-exhausted')
            # Retain reservation even on timeout/failed billing; retries cannot
            # accidentally exceed the budget by assuming failure was unbilled.
            ledger.seek(0, 2)
            ledger.write(json.dumps({'attempt': len(previous) + 1, 'reserved_usd': reserve,
                                     'at_utc': datetime.now(timezone.utc).isoformat()}) + '\n')
            ledger.flush()
        key = self.credential_file.read_text().strip()
        if key.startswith('{'):
            data = json.loads(key)
            key = data.get('OPENAI_API_KEY') or data.get('api_key') or ''
        elif key.startswith(('OPENAI_API_KEY=', 'export OPENAI_API_KEY=')):
            key = key.split('=', 1)[1].strip().strip('\"\'')
        if not key or any(c.isspace() for c in key):
            raise TransportError('credential-format-invalid')
        request = urllib.request.Request(ENDPOINT, data=body, method='POST',
            headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        opener = urllib.request.build_opener(NoRedirect())
        try:
            with opener.open(request, timeout=60) as response:
                return json.loads(response.read(4 * 1024 * 1024))
        except urllib.error.HTTPError as error:
            subtype = ''
            try:
                details = json.loads(error.read(65536)).get('error', {})
                category = details.get('code') or details.get('type')
                if category in {'insufficient_quota', 'rate_limit_exceeded', 'model_not_found'}:
                    subtype = '-' + category
            except (ValueError, TypeError):
                pass
            raise TransportError('openai-http-' + str(error.code) + subtype) from None
        except (urllib.error.URLError, TimeoutError):
            raise TransportError('openai-network-error') from None


def execute(findings, verified_rules, transport):
    safe, aliases = sanitize(findings, verified_rules)
    payload = json.loads(safe)
    request = {'model': MODEL, 'store': False, 'reasoning': {'effort': 'none'}, 'max_output_tokens': MAX_OUTPUT,
               'instructions': (ROOT / 'prompts/triage-system.txt').read_text(), 'input': safe.decode(),
               'text': {'format': {'type': 'json_schema', 'name': 'security_triage', 'strict': True, 'schema': SCHEMA}}}
    body = json.dumps(request, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()
    # Verify final HTTP body as well as the inner sanitizer result.
    if set(request) != {'model', 'store', 'reasoning', 'max_output_tokens', 'instructions', 'input', 'text'} or b'api_key' in body or len(body) > 50000:
        raise Refused('request-refused')
    started = time.monotonic()
    raw = transport(body)
    texts = [c['text'] for item in raw.get('output', []) if item.get('type') == 'message'
             for c in item.get('content', []) if c.get('type') == 'output_text']
    if len(texts) != 1:
        raise TransportError('openai-incomplete-or-refused-output')
    result = validate(json.loads(texts[0]), payload)
    usage = raw.get('usage', {})
    input_tokens, output_tokens = usage.get('input_tokens', 0), usage.get('output_tokens', 0)
    receipt = {'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'model': raw.get('model', MODEL),
               'prompt_version': 'pf-triage-v1', 'request_sha256': hashlib.sha256(body).hexdigest(),
               'response_sha256': hashlib.sha256(texts[0].encode()).hexdigest(), 'findings': len(findings),
               'validation': 'passed', 'duration_seconds': round(time.monotonic() - started, 3),
               'input_tokens': input_tokens, 'output_tokens': output_tokens,
               'estimated_usage_usd': round(input_tokens * INPUT_RATE + output_tokens * OUTPUT_RATE, 8),
               'store': False, 'raw_source_sent': False, 'mode': 'mock' if isinstance(transport, MockTransport) else 'live'}
    return result, aliases, receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--credential-file', type=Path)
    parser.add_argument('--limit', type=int, default=3)
    args = parser.parse_args()
    if args.live and args.dry_run or args.live and not args.credential_file or not 1 <= args.limit <= 20:
        parser.error('Choose explicit live credentials or the default dry-run; limit must be 1..20')
    data = json.loads(args.input.read_text())
    ranked = sorted(data['findings'], key=lambda f: ({'CRITICAL': 0, 'HIGH': 1, 'UNKNOWN': 2, 'MEDIUM': 3, 'LOW': 4, 'INFO': 5}[f['severity']], f['finding_id']))
    chosen = ranked[:args.limit]
    if args.live:
        guard = json.loads((ROOT / 'reports/sanitized/day7/redaction-tests.json').read_text())
        if not guard['passed'] or guard['code_sha256'] != safeguard_digest():
            parser.error('Current captured-body safeguard proof is required')
    transport = OpenAITransport(args.credential_file, ROOT / 'reports/private/day8/budget-ledger.jsonl') if args.live else MockTransport()
    try:
        result, aliases, receipt = execute(chosen, verified_catalog(), transport)
    except (TransportError, Refused, ValueError) as error:
        safe_error = str(error) if isinstance(error, (TransportError, Refused)) else 'triage-response-rejected'
        receipt = {'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'model': MODEL,
                   'prompt_version': 'pf-triage-v1', 'validation': 'not-complete', 'error': safe_error,
                   'mode': 'live' if args.live else 'mock', 'raw_source_sent': False,
                   'billing_purchase_or_topup': False, 'generation_success_claimed': False,
                   'request_sha256': getattr(transport, 'last_request_sha256', None)}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({'receipt': receipt}, indent=2) + '\n')
        public = ROOT / 'reports/sanitized/day8'
        public.mkdir(parents=True, exist_ok=True)
        (public / ('triage-' + receipt['mode'] + '-error.json')).write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt))
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'triage': result, 'receipt': receipt}, indent=2) + '\n')
    args.output.with_suffix('.aliases.json').write_text(json.dumps(aliases, indent=2) + '\n')
    public = ROOT / 'reports/sanitized/day8'
    public.mkdir(parents=True, exist_ok=True)
    (public / ('triage-' + receipt['mode'] + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    raise SystemExit(main())
