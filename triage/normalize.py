"""Normalize hash-bound scanner reports; private locations never become API input."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SEVERITIES = {'INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL', 'UNKNOWN'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(), parse_constant=lambda _: (_ for _ in ()).throw(ValueError('invalid JSON')))


def canonical_location(value):
    value = str(value).replace('\\', '/')
    if 'app/juice-shop/' in value:
        return 'app/juice-shop/' + value.split('app/juice-shop/', 1)[1]
    return value


def adapt(stage, data):
    """Yield rule, severity, component, version, location, line and public fixed versions."""
    if stage == 'sast':
        if not isinstance(data.get('results'), list) or data.get('errors') or not data.get('paths', {}).get('scanned'):
            raise ValueError('invalid or incomplete SAST report')
        for item in data['results']:
            severity = {'ERROR': 'HIGH', 'WARNING': 'MEDIUM', 'INFO': 'LOW'}[item['extra']['severity']]
            yield item['check_id'], severity, '', '', canonical_location(item['path']), item['start']['line'], []
    elif stage in {'sca', 'container'}:
        if data.get('SchemaVersion') != 2 or not data.get('Results'):
            raise ValueError('invalid Trivy report')
        for result in data['Results']:
            for item in result.get('Vulnerabilities') or []:
                yield item['VulnerabilityID'], item['Severity'], item['PkgName'], item['InstalledVersion'], result['Target'], 0, [v.strip() for v in item.get('FixedVersion', '').split(',') if v.strip()]
    elif stage in {'secrets-tree', 'secrets-history'}:
        if not isinstance(data, list):
            raise ValueError('invalid Gitleaks report')
        for item in data:
            # Secret/match/author/email/message fields are deliberately discarded.
            yield item['RuleID'], 'HIGH', '', '', canonical_location(item['File']), item['StartLine'], []
    elif stage == 'iac':
        if data['summary']['parsing_errors'] or data['summary']['skipped'] or data['summary']['resource_count'] < 1:
            raise ValueError('incomplete Checkov report')
        for item in data['results']['failed_checks']:
            yield item['check_id'], 'HIGH', '', '', item['resource'], 0, []
    elif stage == 'dast':
        if not re.fullmatch(r'\d+\.\d+\.\d+', data.get('@version', '')) or not isinstance(data.get('site'), list):
            raise ValueError('invalid ZAP report')
        for site in data['site']:
            for item in site['alerts']:
                risk = {'0': 'INFO', '1': 'LOW', '2': 'MEDIUM', '3': 'HIGH'}[str(item['riskcode'])]
                for instance in item['instances']:
                    # Full URL/evidence is local-only, not an outbound field.
                    yield 'ZAP-' + str(item['pluginid']), risk, '', '', instance['uri'], 0, []
    else:
        raise ValueError('unknown scanner stage')


def normalize(entries):
    findings = {}
    issues = {}
    sources = []
    for stage, path, metadata in entries:
        data = read(path)
        sha = file_sha(path)
        sources.append({'stage': stage, 'sha256': sha, **metadata})
        for index, (rule, severity, component, version, location, line, fixed) in enumerate(adapt(stage, data)):
            if severity not in SEVERITIES:
                raise ValueError('unknown severity')
            family = 'dependency' if stage in {'sca', 'container'} else 'secrets' if stage.startswith('secrets-') else stage
            identity = [family, rule, component, version] if family == 'dependency' else [family, rule, location, line]
            issue_id = 'I-' + digest(identity)[:24]
            observation = [issue_id, stage, location, line]
            finding_id = 'F-' + digest(observation)[:24]
            record = {'stage': stage, 'report_sha256': sha, 'record_index': index, **metadata}
            if finding_id not in findings:
                findings[finding_id] = {'finding_id': finding_id, 'issue_id': issue_id, 'scanner_stage': stage,
                    'rule_id': rule, 'severity': severity, 'original_severity': severity, 'component': component,
                    'version': version, 'fixed_versions': fixed, 'location': location, 'line': line,
                    'first_seen': metadata.get('observed_at_utc'), 'status': 'deferred-study-lab', 'source_records': []}
            findings[finding_id]['source_records'].append(record)
            issues.setdefault(issue_id, {'issue_id': issue_id, 'finding_ids': set(), 'stages': set()})
            issues[issue_id]['finding_ids'].add(finding_id)
            issues[issue_id]['stages'].add(stage)
    result = {'schema_version': 1, 'scope': 'private normalized evidence; not API-safe',
              'generated_at_utc': datetime.now(timezone.utc).isoformat(), 'sources': sources,
              'findings': sorted(findings.values(), key=lambda f: f['finding_id']),
              'issues': [{**issue, 'finding_ids': sorted(issue['finding_ids']), 'stages': sorted(issue['stages'])} for issue in issues.values()]}
    result['counts'] = {'observations': len(findings), 'unique_issues': len(issues),
                        'by_stage': dict(Counter(f['scanner_stage'] for f in findings.values()))}
    return result


def bound_report(manifest_path, entry):
    report = Path(entry['report'])
    if report.is_absolute() or report.name != str(report):
        raise ValueError('unsafe report reference')
    report = manifest_path.parent / report
    expected = entry.get('sha256', entry.get('report_sha256'))
    if not expected or file_sha(report) != expected:
        raise ValueError('report binding mismatch')
    return report


def discover(input_dir):
    entries = []
    index = input_dir / 'pipeline/latest-index.json'
    if index.exists():
        bundle = read(index)
        for item in bundle['reports']:
            path = Path(item['path'])
            if not path.resolve().is_relative_to(input_dir.resolve()) or file_sha(path) != item['sha256']:
                raise ValueError('pipeline report binding mismatch')
            entries.append((item['stage'], path, {k: item.get(k) for k in ['run_id', 'commit', 'observed_at_utc']}))
        return entries
    for marker, stages in [('day3/latest-manifest.txt', {'sast': 'sast', 'sca': 'sca', 'secrets-tree': 'secrets-tree', 'secrets-history': 'secrets-history'}),
                           ('day4/latest-manifest.txt', {'iac-hardened': 'iac', 'dockerfile-hardened': 'iac', 'container-hardened': 'container'})]:
        path = Path((input_dir / marker).read_text().strip())
        manifest = read(path)
        for stage in manifest['stages']:
            if stage['stage'] in stages:
                if stage['execution'] not in {'clean', 'findings', 'complete'}:
                    raise ValueError('scanner execution failed')
                entries.append((stages[stage['stage']], bound_report(path, stage),
                    {'run_id': manifest['run_id'], 'commit': manifest['target_commit'],
                     'observed_at_utc': manifest.get('finished_at_utc')}))
    path = Path((input_dir / 'day5/latest-dast-manifest.txt').read_text().strip())
    manifest = read(path)
    if manifest['execution'] != 'complete':
        raise ValueError('DAST execution failed')
    entries.append(('dast', bound_report(path, manifest), {'run_id': manifest['run_id'], 'observed_at_utc': manifest['observed_at_utc']}))
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path, default=ROOT / 'reports/private')
    parser.add_argument('--output', type=Path, default=ROOT / 'reports/private/normalized.json')
    args = parser.parse_args()
    result = normalize(discover(args.input_dir))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
