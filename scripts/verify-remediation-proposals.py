#!/usr/bin/env python3
"""Prove focused proposals before/after with actual Checkov and isolated lab deployments."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import hashlib

ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy()
ENV['KUBECONFIG'] = ENV.get('PIPELINEFORTRESS_KUBECONFIG', str(ROOT / 'reports/private/day2/kubeconfig'))
KUBE = ['kubectl', '--context', 'kind-pipelinefortress', '--request-timeout=30s']
CHECKOV = ROOT / '.tools/day4/checkov/bin/checkov'
PROBE = "const fs=require('node:fs');Promise.all([fetch('http://127.0.0.1:3000/'),fetch('http://127.0.0.1:3000/rest/products/search?q=apple')]).then(async([a,b])=>{const d=await b.json();if(a.status!==200||b.status!==200||!d.data.length)process.exit(1);console.log(JSON.stringify({home:a.status,products:b.status,product_count:d.data.length,uid:process.getuid(),token_present:fs.existsSync('/var/run/secrets/kubernetes.io/serviceaccount/token')}))}).catch(()=>process.exit(1))"


def call(arguments, **kwargs):
    return subprocess.check_output(arguments, env=ENV, timeout=180, **kwargs)


def main():
    public = ROOT / 'reports/sanitized/day9';public.mkdir(parents=True, exist_ok=True)
    records = []
    for identifier in ['pf-001', 'pf-002', 'pf-003']:
        directory = ROOT / 'reports/private/remediation' / identifier
        proposal = json.loads((directory / 'proposal.json').read_text())
        namespace = 'pipelinefortress-remediation-' + identifier
        record = {'id': identifier, **proposal, 'phases': {}, 'observed_at_utc': datetime.now(timezone.utc).isoformat()}
        with (directory / 'verification.log').open('wb') as log:
            subprocess.run(KUBE + ['create', 'namespace', namespace], env=ENV, check=True, stdout=log, stderr=subprocess.STDOUT)
            try:
                for phase in ['before', 'after']:
                    report = directory / (phase + '-checkov.json')
                    with report.open('wb') as output:
                        result = subprocess.run([str(CHECKOV), '-f', str(directory / (phase + '.yaml')), '--framework', 'kubernetes',
                                                 '--skip-download', '--check', proposal['rule_id'], '-o', 'json'], stdout=output, stderr=log, timeout=180)
                    data = json.loads(report.read_text())
                    expected_code = 1 if phase == 'before' else 0
                    assert result.returncode == expected_code and data['summary']['parsing_errors'] == 0 and data['summary']['skipped'] == 0
                    key = 'failed_checks' if phase == 'before' else 'passed_checks'
                    assert any(c['check_id'] == proposal['rule_id'] for c in data['results'][key])
                    manifest = json.loads(call([str(ROOT / '.tools/day4/checkov/bin/python'), '-c',
                        'import yaml,json,sys;print(json.dumps(yaml.safe_load(open(sys.argv[1]))))', str(directory / (phase + '.yaml'))]))
                    manifest['metadata']['namespace'] = namespace
                    manifest['spec']['template']['metadata'].setdefault('annotations', {})['pipelinefortress/proposal-phase'] = phase
                    rendered = directory / (phase + '-deployment.json');rendered.write_text(json.dumps(manifest))
                    subprocess.run(KUBE + ['apply', '--dry-run=server', '-f', str(rendered)], env=ENV, check=True, stdout=log, stderr=subprocess.STDOUT)
                    subprocess.run(KUBE + ['apply', '-f', str(rendered)], env=ENV, check=True, stdout=log, stderr=subprocess.STDOUT)
                    subprocess.run(KUBE + ['-n', namespace, 'rollout', 'status', 'deployment/juice-shop', '--timeout=150s'], env=ENV, check=True, stdout=log, stderr=subprocess.STDOUT, timeout=180)
                    pods = json.loads(call(KUBE + ['-n', namespace, 'get', 'pods', '-l', 'app.kubernetes.io/name=juice-shop', '-o', 'json']))['items']
                    current = [p for p in pods if not p['metadata'].get('deletionTimestamp') and p['metadata'].get('annotations', {}).get('pipelinefortress/proposal-phase') == phase]
                    assert len(current) == 1 and any(c['type'] == 'Ready' and c['status'] == 'True' for c in current[0]['status']['conditions'])
                    actual = json.loads(call(KUBE + ['-n', namespace, 'exec', current[0]['metadata']['name'], '--', '/nodejs/bin/node', '-e', PROBE]))
                    if phase == 'after' and proposal['operation'] == 'disable-sa-token':assert not actual['token_present']
                    if phase == 'after' and proposal['operation'] == 'require-nonroot':
                        assert current[0]['spec']['securityContext']['runAsNonRoot'] is True and actual['uid'] == 65532
                    if phase == 'after' and proposal['operation'] == 'add-liveness-probe':assert current[0]['spec']['containers'][0]['livenessProbe']['httpGet']['path'] == '/'
                    record['phases'][phase] = {'scanner_exit': result.returncode, 'target_check': 'failed' if phase == 'before' else 'passed',
                                               'scanner_report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(), 'ready': True, 'functional': actual}
            finally:
                subprocess.run(KUBE + ['delete', 'namespace', namespace, '--wait=false'], env=ENV, stdout=log, stderr=subprocess.STDOUT, check=True)
                deleted = subprocess.run(KUBE + ['wait', '--for=delete', 'namespace/' + namespace, '--timeout=90s'], env=ENV, stdout=log, stderr=subprocess.STDOUT, timeout=120)
                record['isolated_namespace_cleanup'] = deleted.returncode == 0
        assert record['isolated_namespace_cleanup']
        records.append(record)
        print(json.dumps({'id': identifier, 'before': 'failed', 'after': 'passed', 'functional': 'passed', 'cleanup': True}), flush=True)
    (public / 'proposals.json').write_text(json.dumps({'proposals': records, 'human_review': 'pending', 'pr_submission': 'pending'}, indent=2) + '\n')


if __name__ == '__main__':
    main()
