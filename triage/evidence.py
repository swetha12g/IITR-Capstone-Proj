"""Small public execution receipts; raw scanner evidence remains local."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import re

from .normalize import adapt

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {'build-test', 'sast', 'sca', 'secrets', 'iac', 'container', 'dast'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def publish(stage, reports, **context):
    if stage not in REQUIRED:
        raise ValueError('unknown evidence stage')
    counts = Counter()
    evidence = []
    fingerprints = set()
    for scanner_stage, path, exit_code in reports:
        valid = {0, 1} if scanner_stage in {'sast', 'iac'} else {0, 20} if scanner_stage in {'sca', 'container', 'secrets-history', 'secrets-tree'} else {0, 1, 2}
        if exit_code not in valid:
            raise ValueError('scanner operational failure')
        data = json.loads(Path(path).read_text())
        if scanner_stage == 'container' and data['Metadata']['ImageID'] != context['image_config_id']:
            raise ValueError('image identity mismatch')
        for rule, severity, component, version, location, line, fixed in adapt(scanner_stage, data):
            counts[severity] += 1
            fingerprints.add(hashlib.sha256(json.dumps([scanner_stage, rule, component, version, location, line]).encode()).hexdigest())
        evidence.append({'scanner_stage': scanner_stage, 'exit_code': exit_code, 'sha256': sha(path)})
    receipt = {'schema_version': 1, 'stage': stage, 'execution': 'complete',
               'run_id': os.environ.get('PIPELINEFORTRESS_RUN_ID', os.environ.get('GITHUB_RUN_ID', 'local')),
               'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
               'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'reports': evidence,
               'findings_by_severity': dict(sorted(counts.items())), 'finding_fingerprints': sorted(fingerprints),
               'profile': 'study-lab', 'deferred_findings': sum(counts.values()), **context}
    public = ROOT / 'reports/sanitized/pipeline'
    public.mkdir(parents=True, exist_ok=True)
    (public / (stage + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    private = ROOT / 'reports/private/pipeline'
    private.mkdir(parents=True, exist_ok=True)
    index = {'run_id': receipt['run_id'], 'commit': receipt['commit'], 'observed_at_utc': receipt['observed_at_utc'],
             'reports': [{'stage': scanner, 'path': str(path), 'sha256': sha(path)} for scanner, path, code in reports]}
    (private / ('latest-' + stage + '.json')).write_text(json.dumps(index, indent=2) + '\n')
    return receipt


def aggregate(directory, needs=None):
    receipts = {}
    errors = []
    if needs is not None and (set(needs) != REQUIRED or any(v.get('result') != 'success' for v in needs.values())):
        errors.append('mandatory-job-did-not-complete')
    for stage in sorted(REQUIRED):
        path = directory / (stage + '.json')
        try:
            value = json.loads(path.read_text())
            if value['schema_version'] != 1 or value['stage'] != stage or value['execution'] != 'complete' or value['profile'] != 'study-lab':
                raise ValueError('invalid receipt')
            if stage != 'build-test' and not value['reports']:
                raise ValueError('missing scanner report binding')
            if any(type(c) is not int or c < 0 for c in value['findings_by_severity'].values()) or not set(value['findings_by_severity']) <= {'INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL', 'UNKNOWN'}:
                raise ValueError('invalid finding counts')
            if any(not re.fullmatch(r'[a-f0-9]{64}', r['sha256']) or type(r['exit_code']) is not int for r in value['reports']):
                raise ValueError('invalid report binding')
            if not re.fullmatch(r'[a-f0-9]{40}', value['commit']):
                raise ValueError('invalid commit binding')
            expected = {'sast': ['sast'], 'sca': ['sca'], 'secrets': ['secrets-history', 'secrets-tree'],
                        'iac': ['iac', 'iac'], 'container': ['container'], 'dast': ['dast'], 'build-test': []}[stage]
            if sorted(r['scanner_stage'] for r in value['reports']) != sorted(expected):
                raise ValueError('missing mandatory report')
            for report in value['reports']:
                valid = {0, 1} if report['scanner_stage'] in {'sast', 'iac'} else {0, 1, 2} if report['scanner_stage'] == 'dast' else {0, 20}
                if report['exit_code'] not in valid:
                    raise ValueError('scanner error exit')
            if stage in {'build-test', 'container', 'dast'} and not re.fullmatch(r'sha256:[a-f0-9]{64}', value.get('image_config_id', '')):
                raise ValueError('invalid image identity')
            receipts[stage] = value
        except (OSError, ValueError, KeyError, TypeError):
            errors.append('missing-or-invalid-' + stage)
    if len(receipts) == len(REQUIRED):
        if len({r['commit'] for r in receipts.values()}) != 1 or len({r['run_id'] for r in receipts.values()}) != 1:
            errors.append('mixed-run-or-commit')
        if len({receipts[s].get('image_config_id') for s in ['build-test', 'container', 'dast']}) != 1:
            errors.append('image-linkage-mismatch')
        if not receipts['dast'].get('routes_verified') or not receipts['dast'].get('cleanup_verified'):
            errors.append('dast-coverage-or-cleanup-missing')
    counts = Counter()
    for receipt in receipts.values():
        counts.update(receipt['findings_by_severity'])
    return {'schema_version': 1, 'profile': 'study-lab', 'verdict': 'ERROR' if errors else 'PASS_WITH_DEFERRED_RISKS' if counts else 'PASS',
            'operational_errors': errors, 'stage_count': len(receipts), 'security_scan_stages': len(REQUIRED) - 1,
            'findings_by_severity': dict(sorted(counts.items())), 'deferred_observations': sum(counts.values()),
            'note': 'Study findings do not stop execution; counts include observations across stages, not deduplicated global issues.',
            'receipts': [{'stage': s, 'sha256': sha(directory / (s + '.json'))} for s in sorted(receipts)]}
