#!/usr/bin/env python3
"""Build from a fresh allowlisted context; never copy local databases or credentials."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'reports/private/day4'
PUBLIC = ROOT / 'reports/sanitized/day4'
DIRECTORIES = {'config', 'data', 'encryptionkeys', 'ftp', 'i18n', 'infrastructure',
               'lib', 'models', 'routes', 'views', '.well-known', 'uploads'}
FILES = {'app.ts', 'server.ts', 'package.json', 'tsconfig.json', 'swagger.yml', 'ctf.key', 'LICENSE'}


def main():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    context = PRIVATE / ('context-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    app = context / 'app'
    names = subprocess.check_output(['git', 'ls-files', '-z', '--', 'app/juice-shop/'], cwd=ROOT).decode().split('\0')
    inputs = {}
    for name in filter(None, names):
        relative = Path(name).relative_to('app/juice-shop')
        permitted = relative.parts[0] in DIRECTORIES or str(relative) in FILES
        permitted |= str(relative).startswith('frontend/src/') or (relative.parts[0] == 'frontend' and len(relative.parts) == 2)
        if not permitted or relative.name == 'package-lock.json':
            continue
        source = ROOT / name
        if source.is_symlink() or not source.is_file():
            raise ValueError('Unexpected source type in build context')
        target = app / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        inputs[str(relative)] = hashlib.sha256(source.read_bytes()).hexdigest()
    for origin, target in [('package-lock.json', 'package-lock.json'),
                           ('frontend-package-lock.json', 'frontend/package-lock.json')]:
        source = ROOT / 'locks/juice-shop' / origin
        shutil.copyfile(source, app / target)
        inputs[target] = hashlib.sha256(source.read_bytes()).hexdigest()
    # Keep the context closed even when local ignored application output exists.
    for directory in ['uploads', 'i18n']:
        (app / directory).mkdir(exist_ok=True)
    for name in ['Dockerfile', 'start.cjs']:
        shutil.copyfile(ROOT / 'infra/docker' / name, context / name)
    (context / '.dockerignore').write_text('**/.git\n**/node_modules\n**/*.sqlite\n**/*.db\n**/.env*\n')
    with (PRIVATE / 'hardened-build.log').open('wb') as output:
        result = subprocess.run(['docker', 'build', '--progress=plain', '-t', 'pipelinefortress:hardened', str(context)],
                                cwd=ROOT, stdout=output, stderr=subprocess.STDOUT, timeout=1800)
    summary = {'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'exit_code': result.returncode,
               'app_source_base_commit': 'f189f521266f42c6bd05884468292000cee852ed',
               'source_variant': 'critical-remediation; runtime input hashes bind local modifications',
               'context_files': len(inputs), 'context_input_sha256': hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest(),
               'locks': {p: inputs[p] for p in ['package-lock.json', 'frontend/package-lock.json']},
               'dockerfile_sha256': hashlib.sha256((context / 'Dockerfile').read_bytes()).hexdigest()}
    if result.returncode == 0:
        image = json.loads(subprocess.check_output(['docker', 'image', 'inspect', 'pipelinefortress:hardened']))[0]
        summary.update(image_config_id=image['Id'], size_bytes=image['Size'], user=image['Config']['User'])
    (PRIVATE / 'build-inputs.json').write_text(json.dumps(inputs, indent=2) + '\n')
    (PUBLIC / 'image-build.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
