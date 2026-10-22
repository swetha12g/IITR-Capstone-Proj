#!/usr/bin/env python3
"""Collect Day 4 comparisons against immutable Docker IDs and one frozen Trivy DB."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / '.tools/day4'
CACHE = ROOT / '.tools/day3/trivy-cache'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    private = ROOT / 'reports/private/day4' / ('scans-' + run_id)
    private.mkdir(parents=True)
    public = ROOT / 'reports/sanitized/day4'
    public.mkdir(parents=True, exist_ok=True)
    home = private / 'home'
    home.mkdir()
    env = os.environ.copy()
    env.update(HOME=str(home), DOCKER_CONFIG=str(home / '.docker'), BC_API_KEY='', BC_SKIP_MAPPING='true',
               SYFT_CHECK_FOR_APP_UPDATE='false', LOG_LEVEL='ERROR')
    for name in ['TRIVY_USERNAME', 'TRIVY_PASSWORD', 'TRIVY_TOKEN', 'CHECKOV_CONFIG_FILE']:
        env.pop(name, None)
    images = {}
    for name in ['baseline', 'hardened']:
        image = json.loads(subprocess.check_output(['docker', 'image', 'inspect', 'pipelinefortress:' + name]))[0]
        images[name] = {'config_id': image['Id'], 'size_bytes': image['Size'], 'user': image['Config']['User']}
    manifest = {'schema_version': 1, 'run_id': run_id, 'started_at_utc': datetime.now(timezone.utc).isoformat(),
                'target_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
                'images': images, 'stages': [], 'inputs': {}}
    for directory in ['infra/k8s', 'infra/k8s-hardened', 'infra/docker', 'policies/checkov']:
        for path in sorted((ROOT / directory).iterdir()):
            if path.is_file():
                manifest['inputs'][str(path.relative_to(ROOT))] = sha(path)
    for name in ['locks/scanners/day4-tools.json', 'locks/scanners/checkov-requirements.txt', 'locks/scanners/cyclonedx-schemas.json',
                 'locks/scanners/tools.json', 'policies/day4-gates.json', 'policies/baseline-exceptions.json', 'locks/juice-shop/package-lock.json',
                 'locks/juice-shop/frontend-package-lock.json', 'scripts/run-day4-scans.py', 'scripts/gate-day4.py',
                 'scripts/test-day4-gates.py', 'scripts/deploy-hardened.py', 'scripts/build-hardened-image.py',
                 'scripts/verify-hardened-runtime.py', 'scripts/verify-day4-policies.py', 'scripts/install-day4-tools.py']:
        manifest['inputs'][name] = sha(ROOT / name)
    path = private / 'manifest.json'

    def persist():
        path.write_text(json.dumps(manifest, indent=2) + '\n')

    def collect(stage, command, expected_codes, image_id=None):
        report = private / (stage + '.json')
        log = private / (stage + '.log')
        started = time.monotonic()
        code = 127
        try:
            with report.open('wb') as out, log.open('wb') as errors:
                # Report writers receive their own filename; Checkov emits JSON on stdout.
                destination = out if stage.startswith(('iac-', 'dockerfile-')) else errors
                result = subprocess.run(command, cwd=ROOT, env=env, stdout=destination, stderr=errors, timeout=900)
                code = result.returncode
        except (OSError, subprocess.TimeoutExpired):
            code = 124
        manifest['stages'].append({'stage': stage, 'exit_code': code, 'execution': 'complete' if code in expected_codes else 'error',
                                   'command': command, 'report': report.name, 'sha256': sha(report), 'log_sha256': sha(log),
                                   'duration_seconds': round(time.monotonic() - started, 2), 'image_config_id': image_id})
        persist()
        print(json.dumps({'stage': stage, 'exit_code': code, 'execution': manifest['stages'][-1]['execution']}), flush=True)

    # Download once, then forbid either image scan from changing databases.
    with (private / 'db-download.log').open('wb') as output:
        result = subprocess.run([str(ROOT / '.tools/day3/trivy'), 'image', '--download-db-only', '--cache-dir', str(CACHE)],
                                env=env, stdout=output, stderr=subprocess.STDOUT, timeout=900)
    if result.returncode:
        raise RuntimeError('Trivy DB update failed; no usable collection claimed')
    metadata = CACHE / 'db/metadata.json'
    manifest['database'] = {'metadata': json.loads(metadata.read_text()), 'sha256': sha(CACHE / 'db/trivy.db')}
    persist()
    for name, directory in [('baseline', 'infra/k8s'), ('hardened', 'infra/k8s-hardened')]:
        collect('iac-' + name, [str(TOOLS / 'checkov/bin/checkov'), '-d', str(ROOT / directory), '--framework', 'kubernetes',
                                '--external-checks-dir', str(ROOT / 'policies/checkov'), '--skip-download', '-o', 'json'], {0, 1})
    for name, dockerfile in [('baseline', 'app/juice-shop/Dockerfile'), ('hardened', 'infra/docker/Dockerfile')]:
        collect('dockerfile-' + name, [str(TOOLS / 'checkov/bin/checkov'), '-f', str(ROOT / dockerfile), '--framework', 'dockerfile',
                                       '--skip-download', '-o', 'json'], {0, 1})
    for name in ['baseline', 'hardened']:
        report = private / ('container-' + name + '.json')
        collect('container-' + name, [str(ROOT / '.tools/day3/trivy'), 'image', '--image-src', 'docker', '--scanners', 'vuln',
                                      '--exit-code', '20', '--format', 'json', '--output', str(report), '--cache-dir', str(CACHE),
                                      '--skip-db-update', '--ignorefile', os.devnull, '--list-all-pkgs', '--timeout', '15m',
                                      images[name]['config_id']], {0, 20}, images[name]['config_id'])
    collect('sbom', [str(TOOLS / 'syft'), 'scan', 'docker:' + images['hardened']['config_id'],
                     '-o', 'cyclonedx-json@1.6=' + str(private / 'sbom.json')], {0}, images['hardened']['config_id'])
    manifest['database_unchanged'] = sha(CACHE / 'db/trivy.db') == manifest['database']['sha256']
    manifest['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    manifest['tools'] = json.loads((public / 'tools-verification.json').read_text())['tools']
    manifest['tools']['trivy'] = json.loads((ROOT / 'locks/scanners/tools.json').read_text())['trivy']['version']
    persist()
    (ROOT / 'reports/private/day4/latest-manifest.txt').write_text(str(path) + '\n')
    safe = {k: manifest[k] for k in ['schema_version', 'run_id', 'target_commit', 'started_at_utc', 'finished_at_utc', 'images', 'database', 'database_unchanged', 'inputs', 'tools']}
    safe['stages'] = [{k: s[k] for k in ['stage', 'execution', 'exit_code', 'sha256', 'duration_seconds', 'image_config_id']} for s in manifest['stages']]
    (public / 'scan-execution.json').write_text(json.dumps(safe, indent=2) + '\n')
    return 0 if manifest['database_unchanged'] and all(s['execution'] == 'complete' for s in manifest['stages']) else 2


if __name__ == '__main__':
    raise SystemExit(main())
