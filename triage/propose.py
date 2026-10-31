"""Bounded local patch templates; model text is never executed or used as a path."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path('infra/k8s/deployment.yaml')
RULES = {'disable-sa-token': 'CKV_K8S_38', 'require-nonroot': 'CKV_K8S_23', 'add-liveness-probe': 'CKV_K8S_8'}


def patch_text(before, operation):
    if operation not in RULES:
        raise ValueError('unsupported patch operation')
    needle = '    spec:\n      containers:\n'
    if before.count(needle) != 1:
        raise ValueError('unexpected baseline manifest shape')
    if operation == 'disable-sa-token':
        if 'automountServiceAccountToken:' in before:
            raise ValueError('control already present')
        after = before.replace(needle, '    spec:\n      automountServiceAccountToken: false\n      containers:\n')
    elif operation == 'require-nonroot':
        if 'runAsNonRoot:' in before:
            raise ValueError('control already present')
        after = before.replace(needle, '    spec:\n      securityContext:\n        runAsNonRoot: true\n        runAsUser: 65532\n        runAsGroup: 65532\n      containers:\n')
    else:
        marker = '          startupProbe:\n'
        if before.count(marker) != 1 or 'livenessProbe:' in before:
            raise ValueError('unexpected probe shape')
        after = before.replace(marker, '          livenessProbe:\n            httpGet:\n              path: /\n              port: http\n            periodSeconds: 15\n            timeoutSeconds: 3\n            failureThreshold: 3\n' + marker)
    if sum(1 for line in difflib.ndiff(before.splitlines(), after.splitlines()) if line.startswith(('+ ', '- '))) > 20:
        raise ValueError('patch exceeds line budget')
    return after


def propose(operation, directory):
    source = ROOT / TARGET
    if source.is_symlink() or not source.is_file():
        raise ValueError('unsafe target')
    directory = directory.resolve()
    if not directory.is_relative_to((ROOT / 'reports/private').resolve()):
        raise ValueError('proposal output must remain private until reviewed')
    before = source.read_text()
    after = patch_text(before, operation)
    directory.mkdir(parents=True, exist_ok=False)
    (directory / 'before.yaml').write_text(before)
    (directory / 'after.yaml').write_text(after)
    diff = ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='a/' + str(TARGET), tofile='b/' + str(TARGET)))
    (directory / 'change.patch').write_text(diff)
    metadata = {'operation': operation, 'rule_id': RULES[operation], 'target': str(TARGET),
                'before_sha256': hashlib.sha256(before.encode()).hexdigest(), 'after_sha256': hashlib.sha256(after.encode()).hexdigest(),
                'patch_sha256': hashlib.sha256(diff.encode()).hexdigest(), 'files_changed': 1,
                'authorship': 'Codex coding assistant authored bounded local template; external triage API attempts returned HTTP 429',
                'external_api_generated_plan_claimed': False, 'applied_to_working_branch': False}
    (directory / 'proposal.json').write_text(json.dumps(metadata, indent=2) + '\n')
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operation', choices=RULES, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(propose(args.operation, args.output_dir)))


if __name__ == '__main__':
    main()
