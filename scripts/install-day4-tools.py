#!/usr/bin/env python3
"""Install verified project-local Day 4 tools; keep Checkov dependencies isolated."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if sys.version_info[:2] != (3, 10) or platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise RuntimeError('Day 4 lock requires Python 3.10 on Linux x86_64')
    pins = json.loads((ROOT / 'locks/scanners/day4-tools.json').read_text())
    tools = ROOT / '.tools/day4'
    private = ROOT / 'reports/private/day4'
    public = ROOT / 'reports/sanitized/day4'
    for directory in [tools, private, public]:
        directory.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    home = private / 'tool-home'
    home.mkdir(exist_ok=True)
    env.update(HOME=str(home), PIP_CONFIG_FILE=os.devnull, PIP_INDEX_URL='https://pypi.org/simple',
               PIP_EXTRA_INDEX_URL='', PIP_CACHE_DIR=str(tools / 'pip-cache'))
    lock = ROOT / pins['checkov']['requirements']
    assert sha(lock) == pins['checkov']['requirements_sha256']
    with (private / 'tool-install.log').open('ab') as output:
        venv = tools / 'checkov'
        if not (venv / 'bin/python').is_file():
            subprocess.run([sys.executable, '-m', 'venv', '--without-pip', str(venv)], check=True, env=env, stdout=output, stderr=subprocess.STDOUT)
        subprocess.run([sys.executable, '-m', 'pip', '--python', str(venv / 'bin/python'), 'install',
                        '--require-hashes', '--only-binary=:all:', '-r', str(lock)],
                       check=True, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=900)
        subprocess.run([sys.executable, '-m', 'pip', '--python', str(venv / 'bin/python'), 'check'],
                       check=True, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=60)
        pin = pins['syft']
        archive = tools / pin['archive']
        if not archive.is_file() or sha(archive) != pin['sha256']:
            subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location', '--connect-timeout', '20',
                            '--max-time', '240', '--retry', '2', pin['url'], '-o', str(archive)], check=True, stdout=output, stderr=subprocess.STDOUT)
        assert sha(archive) == pin['sha256']
        with tarfile.open(archive) as source:
            member = source.getmember('syft')
            assert member.isfile()
            executable = tools / 'syft'
            executable.write_bytes(source.extractfile(member).read())
            executable.chmod(0o755)
        schemas = tools / 'schemas'
        schemas.mkdir(exist_ok=True)
        for name, pin in json.loads((ROOT / 'locks/scanners/cyclonedx-schemas.json').read_text())['schemas'].items():
            target = schemas / name
            if not target.is_file() or sha(target) != pin['sha256']:
                subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location', '--connect-timeout', '20',
                                '--max-time', '120', pin['url'], '-o', str(target)], check=True, stdout=output, stderr=subprocess.STDOUT)
            assert sha(target) == pin['sha256']
    versions = {}
    for name, command in [('checkov', [str(venv / 'bin/checkov'), '--version']),
                          ('syft', [str(tools / 'syft'), 'version', '-o', 'json'])]:
        version = subprocess.check_output(command, env=env, text=True, timeout=60)
        assert pins[name]['version'] in version
        versions[name] = {'version': pins[name]['version'], 'distribution_hash_verified': True}
    summary = {'tools': versions, 'checkov_hashed_distributions': len(lock.read_text().splitlines()),
               'platform': 'linux-x86_64', 'python': '3.10', 'system_installation': False}
    (public / 'tools-verification.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
