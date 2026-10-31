#!/usr/bin/env python3
"""Mutate copies of real scanner outputs to prove Day 4 fails closed."""
import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('day4_gate', ROOT / 'scripts/gate-day4.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def main():
    original = Path((ROOT / 'reports/private/day4/latest-manifest.txt').read_text().strip())
    source = gate.read(original)
    outcomes = []

    def run_case(name, mutation=None, expected_code=None, expected_error=None):
        with tempfile.TemporaryDirectory(prefix='gate-contract-', dir=ROOT / 'reports/private/day4') as temporary:
            directory = Path(temporary)
            manifest = copy.deepcopy(source)
            for stage in manifest['stages']:
                shutil.copyfile(original.parent / stage['report'], directory / stage['report'])
            if mutation:
                mutation(manifest, directory)
            path = directory / 'manifest.json'
            path.write_text(json.dumps(manifest))
            try:
                summary, code = gate.evaluate(path)
                assert expected_error is None and code == expected_code, name
                if name == 'actual-collection-blocks':
                    assert summary['blockers'] > 0 and summary['accepted_day4_risks'] == 0
            except gate.InvalidEvidence as error:
                assert str(error) == expected_error, (name, str(error), expected_error)
                code = 2
            outcomes.append({'case': name, 'passed': True, 'expected_exit': code})

    def change_report(manifest, directory, name, operation):
        stage = next(s for s in manifest['stages'] if s['stage'] == name)
        path = directory / stage['report']
        data = gate.read(path)
        operation(data)
        path.write_text(json.dumps(data))
        stage['sha256'] = gate.sha(path)

    run_case('actual-collection-blocks', expected_code=1)
    run_case('missing-stage', lambda m, d: m['stages'].pop(), expected_error='missing-or-duplicate-stage')
    run_case('scanner-error', lambda m, d: m['stages'][0].update(execution='error', exit_code=124), expected_error='scanner-operational-error')
    run_case('report-tamper', lambda m, d: (d / m['stages'][0]['report']).write_text('{}'), expected_error='report-hash-mismatch')
    run_case('mixed-database', lambda m, d: m.update(database_unchanged=False), expected_error='database-changed-between-images')
    run_case('expired-database', lambda m, d: m['database']['metadata'].update(UpdatedAt=(datetime.now(timezone.utc) - timedelta(days=3)).isoformat()), expected_error='database-stale-or-future')
    run_case('changed-scan-input', lambda m, d: m['inputs'].update({'infra/docker/Dockerfile': '0' * 64}), expected_error='scan-input-changed')
    run_case('wrong-container-image', lambda m, d: change_report(m, d, 'container-hardened', lambda r: r['Metadata'].update(ImageID='sha256:' + '0' * 64)), expected_error='container-wrong-image')
    run_case('wrong-sbom-image', lambda m, d: next(s for s in m['stages'] if s['stage'] == 'sbom').update(image_config_id='sha256:' + '0' * 64), expected_error='sbom-wrong-image')
    run_case('suppressed-control', lambda m, d: change_report(m, d, 'iac-hardened', lambda r: r['summary'].update(skipped=1)), expected_error='iac-parse-or-suppression')

    def missing_custom(m, d):
        def remove(r):
            r['results']['passed_checks'] = [c for c in r['results']['passed_checks'] if c['check_id'] != 'CKV_PF_K8S_1']
            r['summary']['passed'] = len(r['results']['passed_checks'])
        change_report(m, d, 'iac-hardened', remove)
    run_case('missing-custom-check', missing_custom, expected_error='custom-check-did-not-pass')
    run_case('invalid-sbom-schema', lambda m, d: change_report(m, d, 'sbom', lambda r: r.update(components='invalid')), expected_error='sbom-schema-invalid')
    run_case('unsupported-sbom-version', lambda m, d: change_report(m, d, 'sbom', lambda r: r.update(specVersion='invalid')), expected_error='sbom-format-invalid')
    run_case('empty-sbom', lambda m, d: change_report(m, d, 'sbom', lambda r: r.update(components=[])), expected_error='sbom-empty')

    def clean(m, d):
        for name in ['iac-hardened', 'dockerfile-hardened']:
            def no_failed(r):
                for check in r['results'].get('failed_checks', []):
                    check['check_result']['result'] = 'PASSED'
                    r['results']['passed_checks'].append(check)
                r['results']['failed_checks'] = []
                r['summary'].update(failed=0, passed=len(r['results']['passed_checks']))
            change_report(m, d, name, no_failed)
            next(s for s in m['stages'] if s['stage'] == name)['exit_code'] = 0
        change_report(m, d, 'container-hardened', lambda r: [entry.update(Vulnerabilities=[]) for entry in r['Results']])
        next(s for s in m['stages'] if s['stage'] == 'container-hardened')['exit_code'] = 0
    run_case('synthetic-clean-passes', clean, expected_code=0)
    summary = {'passed': True, 'cases': len(outcomes), 'results': outcomes,
               'scope': 'contracts on copied reports; synthetic pass does not change the actual blocked gate'}
    (ROOT / 'reports/sanitized/day4/gate-tests.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'passed': True, 'cases': len(outcomes)}))


if __name__ == '__main__':
    main()
