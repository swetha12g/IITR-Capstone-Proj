#!/usr/bin/env python3
"""Create reproducible user-local tool environments without system package changes."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    if sys.version_info[:2] != (3, 10) or platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise RuntimeError('Recorded locks require Linux x86_64 and Python 3.10')
    private = ROOT / 'reports/private/bootstrap';private.mkdir(parents=True, exist_ok=True)
    tools = ROOT / '.tools/bootstrap';tools.mkdir(parents=True, exist_ok=True)
    pins = json.loads((ROOT / 'locks/bootstrap.json').read_text())
    env = os.environ.copy()
    env.update(PIP_CONFIG_FILE=os.devnull, PIP_INDEX_URL='https://pypi.org/simple', PIP_EXTRA_INDEX_URL='')
    with (private / 'bootstrap.log').open('ab') as log:
        def download(pin, destination):
            if not destination.is_file() or hashlib.sha256(destination.read_bytes()).hexdigest() != pin['sha256']:
                subprocess.run(['curl', '--ipv4', '--fail', '--silent', '--show-error', '--location', '--connect-timeout', '20', '--max-time', '240',
                                pin['url'], '-o', str(destination)], check=True, stdout=log, stderr=subprocess.STDOUT)
            if hashlib.sha256(destination.read_bytes()).hexdigest() != pin['sha256']:
                raise ValueError('bootstrap distribution hash mismatch')
        wheel = tools / pins['pip']['filename'];download(pins['pip'], wheel)
        venv = ROOT / '.venv'
        if not (venv / 'bin/python').is_file():
            subprocess.run([sys.executable, '-m', 'venv', '--without-pip', str(venv)], check=True, stdout=log, stderr=subprocess.STDOUT)
        bootstrap_env = {**env, 'PYTHONPATH': str(wheel)}
        subprocess.run([sys.executable, '-m', 'pip', '--python', str(venv / 'bin/python'), 'install', '--no-index', str(wheel)],
                       check=True, env=bootstrap_env, stdout=log, stderr=subprocess.STDOUT)
        subprocess.run([str(venv / 'bin/python'), '-m', 'pip', 'install', '-r', str(ROOT / 'requirements-dev.txt')],
                       check=True, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=600)
        node_root = ROOT / '.tools/node';node_root.mkdir(exist_ok=True)
        archive = node_root / pins['node']['archive'];download(pins['node'], archive)
        if not (node_root / pins['node']['directory'] / 'bin/node').is_file():
            with tarfile.open(archive) as source:
                for member in source.getmembers():
                    if member.name.startswith('/') or '..' in Path(member.name).parts or not (member.name == pins['node']['directory'] or member.name.startswith(pins['node']['directory'] + '/')):
                        raise ValueError('unsafe Node archive member')
                source.extractall(node_root)
        ci_root = ROOT / '.tools/ci';ci_root.mkdir(exist_ok=True)
        path_file = ci_root / 'paths.txt'
        subprocess.run(['bash', str(ROOT / 'scripts/install-ci-tools.sh')], check=True,
                       env={**env, 'RUNNER_TEMP': str(ci_root), 'GITHUB_PATH': str(path_file)}, stdout=log, stderr=subprocess.STDOUT, timeout=600)
    subprocess.run([str(venv / 'bin/python'), '-m', 'pip', 'check'], check=True)
    node_version = subprocess.check_output([str(node_root / pins['node']['directory'] / 'bin/node'), '--version']).decode().strip()
    assert node_version == 'v24.22.0'
    public = ROOT / 'reports/sanitized/reproduction';public.mkdir(parents=True, exist_ok=True)
    (public / 'bootstrap.json').write_text(json.dumps({'python': '3.10', 'pip': pins['pip']['version'], 'node': node_version,
                                                     'distribution_hashes_verified': True, 'system_packages_changed': False}, indent=2) + '\n')
    print('Project-local Python/Node/kind/kubectl bootstrap verified.')


if __name__ == '__main__':
    main()
