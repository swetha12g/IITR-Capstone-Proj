#!/usr/bin/env python3
"""Exercise actual Checkov custom and built-in checks with negative controls."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CHECKOV = ROOT / '.tools/day4/checkov/bin/checkov'
PRIVATE = ROOT / 'reports/private/day4/policy-fixtures'
PUBLIC = ROOT / 'reports/sanitized/day4'


def environment():
    env = os.environ.copy()
    home = PRIVATE / 'home'
    home.mkdir(parents=True, exist_ok=True)
    env.update(HOME=str(home), BC_SKIP_MAPPING='true', BC_API_KEY='', LOG_LEVEL='ERROR',
               ENABLE_MODULES_FOREACH_HANDLING='false')
    for name in ['PRISMA_API_URL', 'BC_PRISMA_API_URL', 'CHECKOV_CONFIG_FILE']:
        env.pop(name, None)
    return env


def scan(path, output, framework='kubernetes', checks=None):
    command = [str(CHECKOV), '-f', str(path), '--framework', framework, '--external-checks-dir',
               str(ROOT / 'policies/checkov'), '--skip-download', '-o', 'json']
    if checks:
        command += ['--check', ','.join(checks)]
    with output.open('wb') as report, output.with_suffix('.log').open('wb') as log:
        result = subprocess.run(command, cwd=ROOT, env=environment(), stdout=report, stderr=log, timeout=180)
    if result.returncode not in [0, 1]:
        raise RuntimeError('Checkov operational failure')
    data = json.loads(output.read_text())
    if data['summary']['parsing_errors'] or data['summary']['skipped']:
        raise ValueError('Checkov parsing error or suppressed control')
    return result.returncode, data


def main():
    # Use Checkov's pinned YAML parser without changing the project Python dependencies.
    base = json.loads(subprocess.check_output([str(ROOT / '.tools/day4/checkov/bin/python'), '-c',
        'import json,sys,yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1]))))',
        str(ROOT / 'tests/fixtures/day4/restricted-pod.yaml')]))
    PRIVATE.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    cases = []
    for name, image, expected in [('digest', 'example.invalid/app@sha256:' + 'a' * 64, True),
                                   ('latest', 'example.invalid/app:latest', False),
                                   ('version-tag', 'example.invalid/app:1.0.0', False),
                                   ('truncated-digest', 'example.invalid/app@sha256:abc', False),
                                   ('missing-image', None, False)]:
        resource = copy.deepcopy(base)
        if image is None:
            resource['spec']['containers'][0].pop('image')
        else:
            resource['spec']['containers'][0]['image'] = image
        cases.append((name, resource, expected, True))
    resource = copy.deepcopy(base)
    resource['spec']['initContainers'] = [{'name': 'init', 'image': 'example.invalid/app:latest',
                                         'securityContext': copy.deepcopy(base['spec']['containers'][0]['securityContext'])}]
    cases.append(('mutable-init', resource, False, True))
    resource = copy.deepcopy(base)
    resource['spec']['containers'][0]['securityContext']['allowPrivilegeEscalation'] = True
    cases.append(('privilege-escalation', resource, True, False))
    resource = {'apiVersion': 'batch/v1', 'kind': 'CronJob', 'metadata': base['metadata'],
                'spec': {'schedule': '0 0 * * *', 'jobTemplate': {'spec': {'template': {'spec': base['spec']}}}}}
    cases.append(('cronjob-digest', resource, True, True))
    observations = []
    for name, resource, custom_pass, builtin_pass in cases:
        path = PRIVATE / (name + '.yaml')
        path.write_text(json.dumps(resource))
        report = PRIVATE / (name + '.json')
        code, data = scan(path, report, checks=['CKV_PF_K8S_1', 'CKV_K8S_20'])
        passed = {c['check_id'] for c in data['results'].get('passed_checks', [])}
        failed = {c['check_id'] for c in data['results'].get('failed_checks', [])}
        assert ('CKV_PF_K8S_1' in passed) == custom_pass and ('CKV_PF_K8S_1' in failed) != custom_pass, name
        assert ('CKV_K8S_20' in passed) == builtin_pass and ('CKV_K8S_20' in failed) != builtin_pass, name
        assert code == (0 if custom_pass and builtin_pass else 1), name
        observations.append({'case': name, 'exit_code': code, 'passed_ids': sorted(passed), 'failed_ids': sorted(failed),
                             'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest()})
    summary = {'passed': True, 'custom_check_id': 'CKV_PF_K8S_1', 'builtin_check_id': 'CKV_K8S_20', 'cases': observations}
    (PUBLIC / 'policy-fixtures.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'passed': True, 'cases': len(cases), 'custom_check_id': 'CKV_PF_K8S_1'}))


if __name__ == '__main__':
    main()
