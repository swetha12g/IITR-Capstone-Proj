#!/usr/bin/env python3
"""Run pinned passive ZAP against the exact Ready pod in the owned kind network."""
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CLUSTER = os.environ.get('PIPELINEFORTRESS_CLUSTER', 'pipelinefortress')
NODE = CLUSTER + '-control-plane'
KUBE = ['kubectl', '--context', 'kind-' + CLUSTER, '--request-timeout=30s', '-n', 'pipelinefortress']
HOOK = '''import json
def zap_started(zap, target):
    for path in ['/', '/rest/products/search?q=apple', '/rest/languages', '/ftp/', '/metrics', '/rest/products/search?q=%27%29']:
        zap.core.access_url(target + path.lstrip('/'), followredirects=False)
def zap_pre_shutdown(zap):
    with open('/zap/wrk/urls.json', 'w') as output:
        json.dump(zap.core.urls(), output)
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    private = ROOT / 'reports/private/day5' / ('dast-' + run_id)
    private.mkdir(parents=True)
    public = ROOT / 'reports/sanitized/day5'
    public.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['KUBECONFIG'] = env.get('PIPELINEFORTRESS_KUBECONFIG', str(ROOT / 'reports/private/day2/kubeconfig'))
    pods = json.loads(subprocess.check_output(KUBE + ['get', 'pods', '-l', 'app.kubernetes.io/name=juice-shop', '-o', 'json'], env=env))['items']
    pods = [p for p in pods if not p['metadata'].get('deletionTimestamp')]
    assert len(pods) == 1
    pod = pods[0]
    assert any(c['type'] == 'Ready' and c['status'] == 'True' for c in pod['status']['conditions'])
    assert pod['spec']['nodeName'] == NODE
    built = json.loads(subprocess.check_output(['docker', 'image', 'inspect', 'pipelinefortress:hardened']))[0]
    assert pod['metadata']['annotations']['pipelinefortress/image-config-id'] == built['Id']
    cri = json.loads(subprocess.check_output(['docker', 'exec', pod['spec']['nodeName'], 'crictl', 'inspecti', pod['spec']['containers'][0]['image']]))
    assert cri['status']['id'] == built['Id']
    assert pod['status']['containerStatuses'][0]['imageID'].split('@')[-1] in {r.split('@')[-1] for r in cri['status']['repoDigests']}
    target = 'http://' + pod['status']['podIP'] + ':3000/'
    pin = json.loads((ROOT / 'locks/scanners/zap.json').read_text())
    assert '@sha256:' in pin['image']
    shutil.copyfile(ROOT / 'policies/zap/rules.conf', private / 'rules.conf')
    (private / 'hooks.py').write_text(HOOK)
    name = 'pipelinefortress-zap-' + str(os.getpid())
    # Shares only the owned node's private network namespace, with no published
    # scanner ports or host-network API. Bind ZAP API to loopback as well.
    command = ['docker', 'run', '--rm', '--name', name, '--network', 'container:' + NODE,
               '--memory', '2g', '--cpus', '2', '--pids-limit', '256', '-e', 'JAVA_OPTS=-Xmx1536m',
               '-v', str(private) + ':/zap/wrk:rw', pin['image'], 'zap-baseline.py', '--autooff',
               '-t', target, '-P', '18087', '-m', '1', '-T', '5', '-D', '10', '-c', '/zap/wrk/rules.conf',
               '--hook', '/zap/wrk/hooks.py', '-J', 'zap.json', '-r', 'zap.html', '-s',
               '-z', '-host 127.0.0.1 -config api.addrs.addr.name=^(127[.]0[.]0[.]1|0:0:0:0:0:0:0:1|::1|zap)$ -config api.addrs.addr.regex=true -config autoupdate.checkOnStart=false']
    started = time.monotonic()
    code = 3
    try:
        with (private / 'execution.log').open('wb') as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=600)
            code = result.returncode
    except subprocess.TimeoutExpired:
        code = 3
    finally:
        subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    report = private / 'zap.json'
    urls = private / 'urls.json'
    summary = {'schema_version': 1, 'run_id': run_id, 'observed_at_utc': datetime.now(timezone.utc).isoformat(),
               'stage': 'dast', 'exit_code': code, 'execution': 'complete' if code in {0, 1, 2} else 'error',
               'duration_seconds': round(time.monotonic() - started, 2), 'image_config_id': built['Id'],
               'scanner_image': pin['image'], 'policy_sha256': sha(private / 'rules.conf'),
               'scope': 'owned kind Ready pod; unauthenticated traditional crawl and passive scan only',
               'cleanup_container_removed': subprocess.check_output(['docker', 'ps', '-aq', '--filter', 'name=^/' + name + '$']).strip() == b''}
    if report.is_file() and urls.is_file():
        data = json.loads(report.read_text())
        observed = json.loads(urls.read_text())
        assert observed and all(urlsplit(u).hostname == pod['status']['podIP'] for u in observed)
        paths = {urlsplit(u).path for u in observed}
        summary.update(report_sha256=sha(report), urls_sha256=sha(urls), urls_reached=len(observed),
                       seeded_routes_reached={p: p in paths for p in ['/', '/rest/products/search', '/rest/languages', '/ftp/', '/metrics']},
                       alerts_by_risk=dict(Counter(a['riskcode'] for site in data['site'] for a in site['alerts'])),
                       zap_version=data.get('@version'))
        assert all(summary['seeded_routes_reached'].values())
    else:
        summary['execution'] = 'error'
    manifest = {**summary, 'report': 'zap.json', 'urls_report': 'urls.json', 'private_run_dir': str(private)}
    (private / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (ROOT / 'reports/private/day5/latest-dast-manifest.txt').write_text(str(private / 'manifest.json') + '\n')
    (public / 'dast.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))
    return 0 if summary['execution'] == 'complete' and summary['cleanup_container_removed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
