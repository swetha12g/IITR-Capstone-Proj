#!/usr/bin/env python3
"""Collect IaC/container receipts or bind a completed DAST/build receipt."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from triage.evidence import publish, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['iac', 'container', 'dast', 'build-test'], required=True)
    args = parser.parse_args()
    (ROOT / 'reports/sanitized/pipeline' / (args.stage + '.json')).unlink(missing_ok=True)
    private = ROOT / 'reports/private/pipeline' / (args.stage + '-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    private.mkdir(parents=True)
    started = time.monotonic()
    reports = []
    context = {}
    if args.stage in {'build-test', 'container', 'dast'}:
        image = json.loads(subprocess.check_output(['docker', 'image', 'inspect', 'pipelinefortress:hardened']))[0]
        context['image_config_id'] = image['Id']
    if args.stage == 'iac':
        for label, command in [('k8s', ['-d', 'infra/k8s-hardened', '--framework', 'kubernetes', '--external-checks-dir', 'policies/checkov']),
                               ('dockerfile', ['-f', 'infra/docker/Dockerfile', '--framework', 'dockerfile'])]:
            path = private / (label + '.json')
            with path.open('wb') as report, (private / (label + '.log')).open('wb') as log:
                result = subprocess.run([str(ROOT / '.tools/day4/checkov/bin/checkov'), *command, '--skip-download', '-o', 'json'],
                                        cwd=ROOT, stdout=report, stderr=log, timeout=180)
            reports.append(('iac', path, result.returncode))
    elif args.stage == 'container':
        path = private / 'trivy.json'
        with (private / 'trivy.log').open('wb') as log:
            result = subprocess.run([str(ROOT / '.tools/day3/trivy'), 'image', '--image-src', 'docker', '--scanners', 'vuln',
                '--exit-code', '20', '--format', 'json', '--output', str(path), '--cache-dir', str(ROOT / '.tools/day3/trivy-cache'),
                '--ignorefile', '/dev/null', '--list-all-pkgs', '--timeout', '15m', image['Id']], stdout=log, stderr=subprocess.STDOUT, timeout=960)
        reports.append(('container', path, result.returncode))
        with (private / 'syft.log').open('wb') as log:
            subprocess.run([str(ROOT / '.tools/day4/syft'), 'scan', 'docker:' + image['Id'], '-o', 'cyclonedx-json@1.6=' + str(private / 'sbom.json')],
                           check=True, stdout=log, stderr=subprocess.STDOUT, timeout=300)
        import importlib.util
        spec = importlib.util.spec_from_file_location('day4gate', ROOT / 'scripts/gate-day4.py')
        gate = importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
        context['sbom'] = {**gate.validate_sbom(json.loads((private / 'sbom.json').read_text()), ROOT / '.tools/day4/schemas'), 'sha256': sha(private / 'sbom.json')}
    elif args.stage == 'dast':
        path = Path((ROOT / 'reports/private/day5/latest-dast-manifest.txt').read_text().strip())
        manifest = json.loads(path.read_text())
        assert manifest['execution'] == 'complete' and manifest['image_config_id'] == image['Id']
        assert sha(path.parent / manifest['report']) == manifest['report_sha256']
        reports.append(('dast', path.parent / manifest['report'], manifest['exit_code']))
        context.update(routes_verified=all(manifest['seeded_routes_reached'].values()), cleanup_verified=manifest['cleanup_container_removed'],
                       urls_reached=manifest['urls_reached'], scanner_image=manifest['scanner_image'],
                       duration_seconds=manifest['duration_seconds'], duration_scope='ZAP process execution')
        runtime_path = ROOT / 'reports/sanitized/day4/runtime-kubernetes.json'
        runtime = json.loads(runtime_path.read_text())
        assert runtime['passed'] and runtime['image_config_id'] == image['Id']
        context['runtime'] = {'passed': True, 'http_checks_passed': sum(c['passed'] is True for c in runtime['checks']),
                              'http_checks_total': len(runtime['checks']), 'evidence_sha256': sha(runtime_path)}
    else:
        app = json.loads((ROOT / 'reports/sanitized/day1-latest.json').read_text())
        build = json.loads((ROOT / 'reports/sanitized/day4/image-build.json').read_text())
        assert app['status'] == 'passed' and app['locks_unchanged'] and len(app['steps']) == 6
        assert build['exit_code'] == 0 and build['image_config_id'] == image['Id']
        context.update(app_evidence_sha256=sha(ROOT / 'reports/sanitized/day1-latest.json'), build_evidence_sha256=sha(ROOT / 'reports/sanitized/day4/image-build.json'))
        context['app_test_profile'] = app.get('profile', 'upstream-finite')
        context['external_availability_suite'] = app.get('external_availability_suite', 'selected')
        context['test_results'] = {s['step']: s['test_totals'] for s in app['steps'] if 'test_totals' in s}
        server = next(s for s in app['steps'] if s['step'] == 'test-server')
        if 'case_inventory' in server:
            context['server_case_inventory'] = {k: v for k, v in server['case_inventory'].items() if k != 'file_counts'}
        assert context['server_case_inventory']['matched'] and context['server_case_inventory']['reporter_totals_agree']
        junit_path = ROOT / 'reports/private/pipeline/contracts.xml'
        if junit_path.exists():
            suites = list(ET.parse(junit_path).getroot().iter('testsuite'))
            context['contract_tests'] = {key: sum(int(s.get(key, 0)) for s in suites) for key in ['tests', 'failures', 'errors', 'skipped']}
            assert context['contract_tests']['tests'] > 0 and not context['contract_tests']['failures'] and not context['contract_tests']['errors']
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            assert len(context['test_results']) == 3 and 'contract_tests' in context
        context.update(duration_seconds=round(sum(s['duration_seconds'] for s in app['steps']), 2),
                       duration_scope='application check stages only; image build is not timed here')
    context.setdefault('duration_seconds', round(time.monotonic() - started, 2))
    receipt = publish(args.stage, reports, **context)
    print(json.dumps({'stage': args.stage, 'execution': receipt['execution'], 'findings': receipt['findings_by_severity']}))


if __name__ == '__main__':
    main()
