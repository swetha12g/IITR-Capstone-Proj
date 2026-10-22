#!/usr/bin/env python3
"""Deploy the exact local hardened image to the existing owned kind lab."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'reports/private/day4'
ENV = os.environ.copy()
ENV['KUBECONFIG'] = str(Path(ENV.get('PIPELINEFORTRESS_KUBECONFIG', str(ROOT / 'reports/private/day2/kubeconfig'))).resolve())
CLUSTER = ENV.get('PIPELINEFORTRESS_CLUSTER', 'pipelinefortress')
assert re.fullmatch(r'[a-z][a-z0-9-]{0,45}', CLUSTER)
NODE = CLUSTER + '-control-plane'
KUBE = ['kubectl', '--context', 'kind-' + CLUSTER, '--request-timeout=30s']


def main():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    image = json.loads(subprocess.check_output(['docker', 'image', 'inspect', 'pipelinefortress:hardened']))[0]
    nodes = json.loads(subprocess.check_output(KUBE + ['get', 'nodes', '-o', 'json'], env=ENV))['items']
    assert len(nodes) == 1 and nodes[0]['metadata']['name'] == NODE
    subprocess.run(['kind', 'load', 'docker-image', 'pipelinefortress:hardened', '--name', CLUSTER], check=True, env=ENV)
    cri = json.loads(subprocess.check_output(['docker', 'exec', NODE, 'crictl', 'inspecti',
                                            'docker.io/library/pipelinefortress:hardened']))
    assert cri['status']['id'] == image['Id']
    digest = cri['status']['repoDigests'][0].split('@')[1]
    reference = 'docker.io/library/pipelinefortress@' + digest
    assert re.fullmatch(r'[^@\s]+@sha256:[a-f0-9]{64}', reference)
    # kind's generated import name can be unqualified in containerd. Add the
    # canonical digest name that kubelet resolves with imagePullPolicy Never.
    subprocess.run(['docker', 'exec', NODE, 'ctr', '-n', 'k8s.io', 'images',
                    'tag', '--force', 'docker.io/library/pipelinefortress:hardened', reference], check=True)
    resolved = json.loads(subprocess.check_output(['docker', 'exec', NODE, 'crictl', 'inspecti', reference]))
    assert resolved['status']['id'] == image['Id']
    manifest = json.loads(subprocess.check_output(KUBE + ['create', '--dry-run=client', '-f',
                                                         str(ROOT / 'infra/k8s-hardened/deployment.yaml'), '-o', 'json'], env=ENV))
    manifest['spec']['template']['spec']['containers'][0]['image'] = reference
    manifest['spec']['template']['metadata'].setdefault('annotations', {})['pipelinefortress/image-config-id'] = image['Id']
    rendered = PRIVATE / 'deployment-rendered.json'
    rendered.write_text(json.dumps(manifest, indent=2) + '\n')
    for name in ['namespace', 'serviceaccount', 'service']:
        subprocess.run(KUBE + ['apply', '-f', str(ROOT / 'infra/k8s-hardened' / (name + '.yaml'))], check=True, env=ENV)
    subprocess.run(KUBE + ['apply', '--dry-run=server', '-f', str(rendered)], check=True, env=ENV)
    subprocess.run(KUBE + ['apply', '-f', str(rendered)], check=True, env=ENV)
    subprocess.run(KUBE + ['-n', 'pipelinefortress', 'rollout', 'status', 'deployment/juice-shop', '--timeout=300s'], check=True, env=ENV, timeout=330)
    summary = {'image_config_id': image['Id'], 'cri_manifest_reference': reference,
               'rendered_manifest_sha256': hashlib.sha256(rendered.read_bytes()).hexdigest(), 'rollout_passed': True}
    public = ROOT / 'reports/sanitized/day4'
    public.mkdir(parents=True, exist_ok=True)
    (public / 'deployment.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
