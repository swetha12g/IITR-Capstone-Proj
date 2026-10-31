#!/usr/bin/env python3
"""Validate bound Day 4 evidence and block unapproved IaC/container findings."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

from jsonschema import Draft7Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]


class InvalidEvidence(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise InvalidEvidence(code)


def read(path):
    return json.loads(path.read_text(), parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite-json')))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def checkov(data, code):
    require(isinstance(data, dict) and data['summary']['resource_count'] > 0, 'iac-empty-or-invalid')
    summary, results = data['summary'], data['results']
    require(summary['parsing_errors'] == 0 and summary['skipped'] == 0, 'iac-parse-or-suppression')
    for name in ['passed', 'failed', 'skipped']:
        require(summary[name] == len(results.get(name + '_checks', [])), 'iac-incomplete-results')
    require(summary['passed'] + summary['failed'] > 0, 'iac-no-checks')
    require(code == (1 if summary['failed'] else 0), 'iac-exit-mismatch')
    passed = {c['check_id'] for c in results.get('passed_checks', [])}
    failures = [{'check_id': c['check_id'], 'resource': c['resource'],
                 'fingerprint': fingerprint([c['check_id'], c['resource']])} for c in results.get('failed_checks', [])]
    return {'passed': summary['passed'], 'failed': summary['failed'], 'skipped': 0,
            'passed_ids': sorted(passed), 'failures': failures}


def container(data, image_id, code):
    require(data['SchemaVersion'] == 2 and data['Metadata']['ImageID'] == image_id, 'container-wrong-image')
    require(isinstance(data.get('Results'), list) and data['Results'], 'container-empty-analysis')
    require({'os-pkgs', 'lang-pkgs'} <= {r.get('Class') for r in data['Results']}, 'container-incomplete-analysis')
    counts = Counter()
    identities = set()
    blockers = set()
    for result in data['Results']:
        require(isinstance(result.get('Packages'), list) and result['Packages'], 'container-no-package-inventory')
        for item in result.get('Vulnerabilities') or []:
            severity = item['Severity']
            require(severity in {'LOW', 'MEDIUM', 'HIGH', 'CRITICAL', 'UNKNOWN'}, 'container-unknown-severity')
            identity = fingerprint([result['Type'], item['VulnerabilityID'], item['PkgName'], item['InstalledVersion']])
            identities.add(identity)
            counts[severity] += 1
            if severity in {'HIGH', 'CRITICAL', 'UNKNOWN'}:
                blockers.add(identity)
    require(code == (20 if sum(counts.values()) else 0), 'container-exit-mismatch')
    return {'total_occurrences': sum(counts.values()), 'unique_findings': len(identities), 'by_severity': dict(sorted(counts.items())),
            'fingerprints': sorted(identities), 'blocking_fingerprints': sorted(blockers)}


def validate_sbom(data, schema_directory):
    pins = read(ROOT / 'locks/scanners/cyclonedx-schemas.json')['schemas']
    registry = Registry()
    schema = None
    for name, pin in pins.items():
        path = schema_directory / name
        require(sha(path) == pin['sha256'], 'sbom-schema-hash-mismatch')
        document = read(path)
        registry = registry.with_resource(document['$id'], Resource.from_contents(document))
        if name == 'bom-1.6.schema.json':
            schema = document
    require(schema is not None, 'sbom-schema-missing')
    require(not any(Draft7Validator(schema, registry=registry).iter_errors(data)), 'sbom-schema-invalid')
    require(data.get('bomFormat') == 'CycloneDX' and data.get('specVersion') == '1.6', 'sbom-format-invalid')
    components = data.get('components', [])
    require(len(components) > 0, 'sbom-empty')
    lock = read(ROOT / 'locks/juice-shop/package-lock.json')
    expected = {'juice-shop': lock['version'], 'express': lock['packages']['node_modules/express']['version'],
                'sqlite3': lock['packages']['node_modules/sqlite3']['version']}
    for name, version in expected.items():
        require(any(c.get('name') == name and c.get('version') == version for c in components), 'sbom-package-mismatch')
    for name in ['express', 'sqlite3']:
        require(any(c.get('name') == name and any(p['name'].startswith('syft:location:') and
                    p['value'] == '/juice-shop/node_modules/' + name + '/package.json' for p in c.get('properties', []))
                    for c in components), 'sbom-no-installed-package-evidence')
    return {'schema_valid': True, 'spec_version': '1.6', 'components': len(components), 'representative_packages': expected}


def evaluate(path, schema_directory=None, now=None, profile='strict'):
    manifest = read(path)
    policy = read(ROOT / 'policies/day4-gates.json')
    require(profile in {'strict', 'study-lab'}, 'unknown-gate-profile')
    require(manifest.get('schema_version') == 1, 'invalid-manifest-version')
    require(policy['exceptions'] == [], 'day4-risk-acceptance-not-implemented')
    require(policy['block_all_failed_iac_checks'] is True and set(policy['blocking_container_severities']) == {'HIGH', 'CRITICAL', 'UNKNOWN'}, 'unsupported-gate-policy')
    require(bool(re.fullmatch(r'[a-f0-9]{40}', manifest['target_commit'])), 'invalid-target-commit')
    approved_source = subprocess.check_output(['git', 'show', manifest['target_commit'] + ':policies/baseline-exceptions.json'], cwd=ROOT, stderr=subprocess.DEVNULL)
    require(sha(ROOT / 'policies/baseline-exceptions.json') == hashlib.sha256(approved_source).hexdigest(), 'source-risk-approvals-changed')
    require(manifest['database_unchanged'] is True, 'database-changed-between-images')
    now = now or datetime.now(timezone.utc)
    timestamp = re.sub(r'(\.\d{6})\d+', r'\1', manifest['database']['metadata']['UpdatedAt'])
    updated = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    require(-1 <= (now - updated).total_seconds() / 3600 <= policy['maximum_database_age_hours'], 'database-stale-or-future')
    for name, digest in manifest['inputs'].items():
        relative = Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe-input-path')
        require(sha(ROOT / relative) == digest, 'scan-input-changed')
    stages = {s['stage']: s for s in manifest['stages']}
    require(len(stages) == len(manifest['stages']) and set(stages) == set(policy['required_stages']), 'missing-or-duplicate-stage')
    reports = {}
    for name, stage in stages.items():
        require(stage['execution'] == 'complete', 'scanner-operational-error')
        expected = {0, 1} if name.startswith(('iac-', 'dockerfile-')) else {0, 20} if name.startswith('container-') else {0}
        require(stage['exit_code'] in expected, 'scanner-invalid-exit')
        report = Path(stage['report'])
        require(not report.is_absolute() and report.name == str(report), 'unsafe-report-path')
        report = path.parent / report
        require(sha(report) == stage['sha256'], 'report-hash-mismatch')
        reports[name] = read(report)
    images = manifest['images']
    for name in ['baseline', 'hardened']:
        require(bool(re.fullmatch(r'sha256:[a-f0-9]{64}', images[name]['config_id'])), 'invalid-image-config-id')
        require(stages['container-' + name]['image_config_id'] == images[name]['config_id'], 'stage-image-mismatch')
    require(stages['sbom']['image_config_id'] == images['hardened']['config_id'], 'sbom-wrong-image')
    require('docker:' + images['hardened']['config_id'] in stages['sbom']['command'], 'sbom-source-not-immutable')
    iac = {name: checkov(reports[name], stages[name]['exit_code']) for name in ['iac-baseline', 'iac-hardened', 'dockerfile-baseline', 'dockerfile-hardened']}
    require(policy['required_custom_check'] in iac['iac-hardened']['passed_ids'], 'custom-check-did-not-pass')
    scans = {name: container(reports['container-' + name], images[name]['config_id'], stages['container-' + name]['exit_code']) for name in ['baseline', 'hardened']}
    sbom = validate_sbom(reports['sbom'], schema_directory or ROOT / '.tools/day4/schemas')
    sbom['sha256'] = stages['sbom']['sha256']
    sbom['image_config_id'] = images['hardened']['config_id']
    old, new = set(scans['baseline']['fingerprints']), set(scans['hardened']['fingerprints'])
    old_iac = {c['fingerprint'] for name in ['iac-baseline', 'dockerfile-baseline'] for c in iac[name]['failures']}
    new_iac = {c['fingerprint'] for name in ['iac-hardened', 'dockerfile-hardened'] for c in iac[name]['failures']}
    blockers = len(new_iac) + len(scans['hardened']['blocking_fingerprints'])
    summary = {'schema_version': 1, 'run_id': manifest['run_id'], 'target_commit': manifest['target_commit'],
               'verdict': 'BLOCK' if blockers else 'PASS', 'operational_errors': [], 'blockers': blockers,
               'accepted_day4_risks': 0, 'source_exceptions_unchanged': True, 'images': images,
               'iac': iac, 'container': scans, 'sbom': sbom, 'database': manifest['database'],
               'comparison': {'iac_removed': len(old_iac - new_iac), 'iac_added': len(new_iac - old_iac),
                              'container_removed': len(old - new), 'container_added': len(new - old), 'container_retained': len(old & new),
                              'image_size_reduction_bytes': images['baseline']['size_bytes'] - images['hardened']['size_bytes']}}
    summary['profile'] = profile
    summary['deferred_findings'] = blockers if profile == 'study-lab' else 0
    if profile == 'study-lab':
        require(policy['study_lab']['scope'] == 'owned study lab only; no production promotion', 'invalid-study-scope')
        summary['strict_verdict'] = summary['verdict']
        summary['verdict'] = 'PASS_WITH_DEFERRED_RISKS' if blockers else 'PASS'
        summary['blockers'] = 0
        summary['study_decision'] = policy['study_lab']
        return summary, 0
    return summary, 1 if blockers else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--profile', choices=['strict', 'study-lab'], default='study-lab')
    parser.add_argument('--output', type=Path, default=ROOT / 'reports/sanitized/day4/gate-summary.json')
    args = parser.parse_args()
    try:
        summary, code = evaluate(args.manifest, profile=args.profile)
    except Exception as error:
        summary = {'verdict': 'ERROR', 'operational_errors': [str(error) if isinstance(error, InvalidEvidence) else 'missing-or-invalid-evidence'], 'blockers': None}
        code = 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: summary[k] for k in ['verdict', 'blockers', 'operational_errors']}))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
