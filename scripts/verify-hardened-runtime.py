#!/usr/bin/env python3
"""Verify the exact hardened image, enforced controls and lab application behavior."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'reports/private/day4'
PUBLIC = ROOT / 'reports/sanitized/day4'
WRITABLE = ['data', 'ftp', 'i18n', 'frontend/dist', 'uploads', 'logs', '.well-known']
HTTP = build_opener(ProxyHandler({}))
ENV = os.environ.copy()
ENV['KUBECONFIG'] = str(Path(ENV.get('PIPELINEFORTRESS_KUBECONFIG', str(ROOT / 'reports/private/day2/kubeconfig'))).resolve())
KUBE = ['kubectl', '--context', 'kind-' + ENV.get('PIPELINEFORTRESS_CLUSTER', 'pipelinefortress'), '-n', 'pipelinefortress']
PROBE = r"""
const fs=require('node:fs'); const assert=require('node:assert/strict');
const status=fs.readFileSync('/proc/1/status','utf8');
const fields=Object.fromEntries(status.split('\n').filter(l=>/^(Uid|Gid|CapEff|CapBnd|NoNewPrivs|Seccomp):/.test(l)).map(l=>{const [k,...v]=l.split(/:\s*/);return[k,v.join(':')]}));
assert.equal(process.getuid(),65532); assert.equal(process.getgid(),65532);
assert.equal(fields.CapEff,'0000000000000000'); assert.equal(fields.CapBnd,'0000000000000000');
assert.equal(fields.NoNewPrivs,'1'); assert.equal(fields.Seccomp,'2');
const readonly=[];
for(const dir of ['/juice-shop','/juice-shop/build','/opt/juice-shop-seed']) {
 const p=dir+'/.pipelinefortress-write-probe';
 try {fs.writeFileSync(p,'test',{flag:'wx'});fs.unlinkSync(p);throw Error('Root unexpectedly writable');}
 catch(e) {assert.equal(e.code,'EROFS');readonly.push(dir);}
}
const writable=[];
for(const dir of ['data','ftp','i18n','frontend/dist','uploads','logs','.well-known']) {
 const p='/juice-shop/'+dir+'/.pipelinefortress-write-probe'; fs.writeFileSync(p,'test',{flag:'wx'});fs.unlinkSync(p);writable.push(dir);
}
const token='/var/run/secrets/kubernetes.io/serviceaccount/token';assert.equal(fs.existsSync(token),false);
assert.equal(fs.existsSync('/bin/sh'),false);assert.equal(fs.existsSync('/usr/bin/npm'),false);
console.log(JSON.stringify({uid:process.getuid(),gid:process.getgid(),process:fields,readonly,writable,service_account_token_absent:true,shell_and_npm_absent:true}));
"""


def output(command):
    return subprocess.check_output(command, env=ENV, timeout=60)


def inspect(command):
    return json.loads(output(command))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['docker', 'kubernetes'], required=True)
    args = parser.parse_args()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    image = inspect(['docker', 'image', 'inspect', 'pipelinefortress:hardened'])[0]
    summary = {'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'mode': args.mode,
               'image_config_id': image['Id'], 'image_size_bytes': image['Size'], 'checks': []}
    container = None
    forward = None
    try:
        if args.mode == 'docker':
            name = 'pipelinefortress-day4-' + str(os.getpid())
            command = ['docker', 'run', '-d', '--name', name, '--read-only', '--user', '65532:65532',
                       '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true', '--memory', '768m',
                       '--cpus', '1', '--pids-limit', '256', '-p', '127.0.0.1::3000']
            for directory in WRITABLE:
                command += ['--tmpfs', '/juice-shop/' + directory + ':rw,nosuid,nodev,noexec,uid=65532,gid=65532,mode=0750,size=128m']
            command += ['--tmpfs', '/tmp:rw,nosuid,nodev,noexec,uid=65532,gid=65532,mode=0700,size=64m', image['Id']]
            container = output(command).decode().strip()
            state = inspect(['docker', 'inspect', container])[0]
            assert state['Image'] == image['Id']
            port = state['NetworkSettings']['Ports']['3000/tcp'][0]['HostPort']
            execute = ['docker', 'exec', container, '/nodejs/bin/node', '-e']
            summary['enforcement'] = {k: state['HostConfig'][k] for k in ['ReadonlyRootfs', 'CapDrop', 'SecurityOpt', 'Memory', 'NanoCpus', 'PidsLimit']}
        else:
            pods = inspect(KUBE + ['get', 'pods', '-l', 'app.kubernetes.io/name=juice-shop', '-o', 'json'])['items']
            pods = [p for p in pods if not p['metadata'].get('deletionTimestamp')]
            assert len(pods) == 1
            pod = pods[0]
            assert any(c['type'] == 'Ready' and c['status'] == 'True' for c in pod['status']['conditions'])
            assert pod['metadata']['annotations']['pipelinefortress/image-config-id'] == image['Id']
            running = pod['status']['containerStatuses'][0]
            cri = inspect(['docker', 'exec', pod['spec']['nodeName'], 'crictl', 'inspecti', pod['spec']['containers'][0]['image']])
            assert cri['status']['id'] == image['Id']
            # containerd can retain kind's original import repository name in
            # status. Compare the manifest digest as well as the config ID.
            assert running['imageID'].split('@')[-1] in {r.split('@')[-1] for r in cri['status']['repoDigests']}
            spec = pod['spec']
            app = spec['containers'][0]
            assert spec['automountServiceAccountToken'] is False
            assert spec['securityContext']['runAsNonRoot'] is True
            assert spec['securityContext']['seccompProfile']['type'] == 'RuntimeDefault'
            assert app['securityContext']['allowPrivilegeEscalation'] is False
            assert app['securityContext']['readOnlyRootFilesystem'] is True
            assert app['securityContext']['capabilities']['drop'] == ['ALL']
            summary['enforcement'] = {'pod_security_context': spec['securityContext'], 'container_security_context': app['securityContext'],
                                      'resources': app['resources'], 'automountServiceAccountToken': False,
                                      'cri_manifest_reference': running['imageID'], 'cri_config_id': cri['status']['id'],
                                      'restarts': running['restartCount']}
            execute = KUBE + ['exec', pod['metadata']['name'], '--', '/nodejs/bin/node', '-e']
            port = '3004'
            log = (PRIVATE / 'hardened-port-forward.log').open('wb')
            forward = subprocess.Popen(KUBE + ['port-forward', '--address', '127.0.0.1', 'pod/' + pod['metadata']['name'], port + ':3000'],
                                       env=ENV, stdout=log, stderr=subprocess.STDOUT)
        endpoint = 'http://127.0.0.1:' + port
        for _ in range(90):
            if container and not inspect(['docker', 'inspect', container])[0]['State']['Running']:
                raise RuntimeError('Hardened container exited; inspect private startup log')
            try:
                with HTTP.open(endpoint + '/', timeout=3) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError, ConnectionError):
                time.sleep(1)
        else:
            raise RuntimeError('Hardened application did not become ready')
        summary['controls'] = inspect(execute + [PROBE])
        checks = [
            ('http-home', '/', lambda s, b: s == 200 and b'<html' in b.lower()),
            ('products', '/rest/products/search?q=apple', lambda s, b: s == 200 and bool(json.loads(b)['data'])),
            ('languages', '/rest/languages', lambda s, b: s == 200 and b'en' in b),
            ('coding-challenge', '/snippets/unionSqlInjectionChallenge', lambda s, b: s == 200 and b'snippet' in b),
            ('training-directory-listing', '/ftp/', lambda s, b: s == 200 and b'acquisitions.md' in b),
            ('training-metrics', '/metrics', lambda s, b: s == 200 and b'# HELP' in b),
            ('training-sql-error', '/rest/products/search?q=%27%29', lambda s, b: s == 500 and b'SQLITE_ERROR' in b and b'stack' in b),
        ]
        for identifier, path, predicate in checks:
            try:
                response = HTTP.open(endpoint + path, timeout=15)
            except HTTPError as error:
                response = error
            with response:
                body = response.read(4 * 1024 * 1024)
                status = response.status
            (PRIVATE / (args.mode + '-' + identifier + '.response')).write_bytes(body)
            summary['checks'].append({'id': identifier, 'http_status': status, 'passed': bool(predicate(status, body)),
                                      'response_sha256': hashlib.sha256(body).hexdigest()})
        summary['passed'] = all(c['passed'] for c in summary['checks'])
    finally:
        if forward:
            forward.terminate()
            forward.wait(timeout=15)
            log.close()
        if container:
            logs = subprocess.run(['docker', 'logs', container], capture_output=True)
            (PRIVATE / 'hardened-docker.log').write_bytes(logs.stdout + logs.stderr)
            subprocess.run(['docker', 'rm', '-f', container], check=True, stdout=subprocess.DEVNULL)
    (PUBLIC / ('runtime-' + args.mode + '.json')).write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'mode': args.mode, 'passed': summary['passed'], 'checks': summary['checks']}))
    return 0 if summary['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
