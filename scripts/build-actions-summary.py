#!/usr/bin/env python3
"""Publish a numeric, commit-bound Actions report, including on failed runs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from triage.evidence import aggregate, REQUIRED

ORDER = ['build-test', 'sast', 'sca', 'secrets', 'iac', 'container', 'dast']
SEVERITIES = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO', 'UNKNOWN']


def safe_hash(value, length=64):
    return value if isinstance(value, str) and re.fullmatch(r'[a-f0-9]{' + str(length) + '}', value) else 'unavailable'


def number(value):
    return str(value) if type(value) is int and value >= 0 else 'unavailable'


def report(directory, *, run_id, commit, repository, needs):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) or not re.fullmatch(r'\d+', run_id) or safe_hash(commit, 40) == 'unavailable':
        raise ValueError('invalid GitHub execution identity')
    verdict = aggregate(directory, needs)
    records = {}
    identity_errors = []
    for stage in ORDER:
        try:
            value = json.loads((directory / (stage + '.json')).read_text())
            if value.get('run_id') != run_id or value.get('commit') != commit or value.get('stage') != stage:
                identity_errors.append('current-run-identity-mismatch-' + stage)
                continue
            records[stage] = value
        except (ValueError, OSError, AttributeError):
            continue
    errors = verdict['operational_errors'] + identity_errors
    clean = not errors and not verdict['security_blockers']
    base = 'https://github.com/' + repository
    source = base + '/blob/' + commit + '/'
    run = base + '/actions/runs/' + run_id
    state = '✅ ZERO CRITICAL · STUDY GATE PASSED' if clean else '❌ STUDY GATE FAILED / INCOMPLETE'
    critical = number(verdict['critical_observations']) if not errors else 'UNVERIFIED'
    lines = [
        '# 🛡️ PipelineFortress | Critical repair & CI report', '',
        '> **' + state + '**', '',
        f'[This workflow run]({run}) · [Tested commit `{commit[:12]}`]({base}/commit/{commit}) · '
        f'[Full study PDF]({source}output/pdf/PipelineFortress_Study_Report.pdf)', '',
        '| Critical observations | Mandatory receipts | Security stages | Operational errors |',
        '| :---: | :---: | :---: | :---: |',
        f"| **{critical}** | **{verdict['stage_count']} / 7** | **6 required** | **{len(errors)}** |", '',
        '**Scope:** educational study lab. Critical findings fail CI. High and lower findings remain visible and deferred; a passing study gate does not establish production readiness.', '',
        '## 1 · Fresh hosted security results', '',
        '| Stage | Job | Receipt | Critical | High | Medium | Low | Info | Unknown | Measured seconds |',
        '| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |',
    ]
    for stage in ORDER:
        record = records.get(stage, {})
        counts = record.get('findings_by_severity', {})
        job = needs.get(stage, {}).get('result', 'unavailable')
        job = job if job in {'success', 'failure', 'cancelled', 'skipped'} else 'unavailable'
        duration = record.get('duration_seconds')
        seconds = f'{duration:.2f}' if type(duration) in {int, float} and 0 <= duration < 100000 else 'unavailable'
        values = [number(counts.get(s, 0)) if record else '—' for s in SEVERITIES]
        status = 'complete' if record.get('execution') == 'complete' else 'missing/invalid'
        lines.append('| ' + ' | '.join([stage, job, status, *values, seconds]) + ' |')
    counts = verdict['findings_by_severity']
    lines += ['', '| Current cross-stage totals | Critical | High | Medium | Low | Info | Unknown |',
              '| --- | ---: | ---: | ---: | ---: | ---: | ---: |',
              '| Observations | ' + ' | '.join(number(counts.get(s, 0)) for s in SEVERITIES) + ' |', '',
              '**Counting rule:** these are scanner observations, including duplicates across source/image and history/tree scans. They are not globally deduplicated issues. Missing or mismatched evidence never proves zero. Durations are stage scopes, not workflow wall time.', '',
              '## 2 · Application & pipeline verification', '',
              '| Test suite | Passed | Failed | Skipped | Cancelled / todo |',
              '| --- | ---: | ---: | ---: | ---: |']
    build = records.get('build-test', {})
    tests = build.get('test_results', {})
    for suite in ['test-frontend', 'test-server', 'test-api']:
        totals = tests.get(suite, {})
        lines.append('| ' + ' | '.join([suite, *(number(totals.get(k)) for k in ['passed', 'failed', 'skipped']),
                                        number(totals.get('cancelled')) + ' / ' + number(totals.get('todo'))]) + ' |')
    contracts = build.get('contract_tests', {})
    lines += ['', f"Pipeline / AI boundary / report contracts: **{number(contracts.get('tests'))} tests**, "
              f"{number(contracts.get('failures'))} failures, {number(contracts.get('errors'))} errors, {number(contracts.get('skipped'))} skipped.", '',
              'A successful build-test job includes pinned installs, frontend/backend build, selected local application tests, lint and snippet consistency. The independent internet-resource availability suite is excluded; other skips are shown above. Legacy Cypress challenge E2E coverage is not claimed.', '',
              '## 3 · Exact-image inventory, runtime & passive DAST', '',
              '| Evidence | Result |', '| --- | --- |']
    container = records.get('container', {})
    dast = records.get('dast', {})
    sbom = container.get('sbom', {})
    runtime = dast.get('runtime', {})
    flag = lambda value: 'verified' if value is True else 'unverified'
    lines += [f"| CycloneDX SBOM schema | {flag(sbom.get('schema_valid'))} |",
              f"| Image components | {number(sbom.get('components'))} |",
              f"| Kubernetes HTTP checks | {number(runtime.get('http_checks_passed'))} / {number(runtime.get('http_checks_total'))} |",
              f"| Passive DAST URLs reached | {number(dast.get('urls_reached'))} |",
              f"| Required seeded routes | {flag(dast.get('routes_verified'))} |",
              f"| Scanner container cleanup | {flag(dast.get('cleanup_verified'))} |", '',
              'Runtime checks cover the owned ephemeral Kubernetes deployment. Controls include non-root execution, a read-only root filesystem, dropped capabilities, no privilege escalation and absent service-account token. The DAST job also proves bad/fixed passive-header fixtures and removes its owned cluster in an always-run cleanup step; inspect its job result for cleanup failures. Passive unauthenticated crawling does not cover every route or authenticated attack.', '',
              '## 4 · Critical repair record', '',
              'The pre-repair local register held **11 unique critical issues** (22 source/image observations). The dependency families below were repaired and regression-tested before publication; the live table above is the authoritative result for this commit.', '',
              '| Family | Repair |', '| --- | --- |',
              '| JWT / express-jwt | jsonwebtoken 9.0.3, express-jwt 8.5.1; explicit RS256 and generated 2048-bit keys |',
              '| MarsDB | Replaced with @seald-io/nedb 4.1.2; executable selectors rejected, typed queries |',
              '| decompress / download | Removed extraction dependency; bounded streamed HTTP download |',
              '| Handlebars | 4.7.10 override |',
              '| crypto-js | 4.2.0 override |',
              '| Lodash / sanitizer | sanitize-html 2.18.1; vulnerable Lodash 2.x path removed |',
              '| tar | 7.5.19 override |', '',
              f'[Detailed repair and negative-probe evidence]({source}docs/critical-remediation.md) · '
              f'[Local verification snapshot]({source}reports/sanitized/critical-remediation/verification.json)', '',
              'The separate pre-commit local snapshot reported **180 unique issues: 0 critical, 91 high, 45 medium, 28 low, 16 informational**, with 2,332 application passes and six skips. Those historical unique totals are not substituted for this run’s observation counts. Its old/new immutable-image probes demonstrated rejection of unsigned JWTs and executable selectors. Signing keys rotate on process restart, requiring renewed sessions.', '',
              '## 5 · Deferred work & assessment limits', '',
              f'- High/lower fixes: [deferred issue register]({source}docs/deferred-remediation.md).',
              '- Successful live AI evaluation remains pending after three HTTP429 attempts; automatic request cap exhausted. This workflow makes no provider calls or purchases.',
              '- Independent labels, human PR review and oral assessment remain outstanding. No reviewer approval or production certification is inferred.',
              '- Secret scans retain intentional upstream training fixtures and history. Raw scanner matches, credentials, private logs and full SBOM contents are excluded from this report artifact.', '',
              f'[Project completion and remaining evidence]({source}docs/project-completion.md) · '
              f'[Evidence index]({source}docs/evidence-index.md) · '
              f'[Dashboard snapshot source]({source}reports/sanitized/dashboard/index.html)', '',
              '## 6 · Download & audit trail', '',
              f'Download **aggregate-study-evidence** from [this run’s artifacts]({run}#artifacts): this exact Markdown poster, all seven sanitized stage receipts, aggregate JSON, the twelve-page study PDF, and the dashboard HTML/JSON/CSV. The PDF and dashboard are checked-in evidence snapshots with their own run scopes; this Actions Summary records the fresh hosted execution.', '',
              '<details>', '<summary>Commit, image, source tree and receipt hashes</summary>', '',
              f'- Run: `{run_id}`', f'- Commit: `{commit}`',
              '- Source tree: `' + safe_hash(build.get('project_tree_sha256')) + '`',
              '- Image config: `' + ('sha256:' + safe_hash(build.get('image_config_id', '').removeprefix('sha256:'))) + '`', '',
              '| Stage receipt | SHA-256 |', '| --- | --- |']
    for item in verdict['receipts']:
        lines.append('| ' + item['stage'] + ' | `' + safe_hash(item['sha256']) + '` |')
    lines += ['', '</details>', '']
    if errors or verdict['security_blockers']:
        lines += ['## Execution / security failures', '', 'The gate did not establish a passing zero-critical result. Resolve these errors and rerun CI:', '']
        for error in errors + verdict['security_blockers']:
            lines.append('- `' + (error if re.fullmatch(r'[a-z0-9-]+', error) else 'invalid-evidence') + '`')
    return '\n'.join(lines) + '\n', not clean


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipts', type=Path, default=ROOT / 'reports/sanitized/pipeline')
    args = parser.parse_args()
    text, failed = report(args.receipts, run_id=os.environ['GITHUB_RUN_ID'], commit=os.environ['GITHUB_SHA'],
                          repository=os.environ['GITHUB_REPOSITORY'], needs=json.loads(os.environ['PIPELINEFORTRESS_JOB_RESULTS']))
    output = ROOT / 'reports/sanitized/actions-summary.md'
    output.write_text(text)
    payload = text.encode()
    if len(payload) >= 1024 * 1024:
        raise ValueError('Actions summary exceeds the per-step limit')
    with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a') as stream:
        stream.write(text)
    print(json.dumps({'summary_bytes': len(payload), 'summary_sha256': hashlib.sha256(payload).hexdigest(), 'gate_failed': failed}))
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
