#!/usr/bin/env python3
"""Export/import only the clean hardened image with archive and config verification."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['export', 'import'])
    parser.add_argument('--directory', type=Path, default=ROOT / 'reports/private/image-transfer')
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    archive = args.directory / 'hardened.tar.gz'
    metadata = args.directory / 'image.json'
    if args.mode == 'export':
        image = json.loads(subprocess.check_output(['docker', 'image', 'inspect', 'pipelinefortress:hardened']))[0]
        process = subprocess.Popen(['docker', 'save', 'pipelinefortress:hardened'], stdout=subprocess.PIPE)
        with gzip.open(archive, 'wb', compresslevel=3) as output:
            while chunk := process.stdout.read(1024 * 1024):
                output.write(chunk)
        if process.wait():
            raise RuntimeError('image export failed')
        data = {'image_config_id': image['Id'], 'archive_sha256': hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(archive.read_bytes()).hexdigest(),
                'scope': 'allowlisted source build only; no workstation credentials/raw scanner reports'}
        metadata.write_text(json.dumps(data, indent=2) + '\n')
    else:
        data = json.loads(metadata.read_text())
        if hashlib.sha256(archive.read_bytes()).hexdigest() != data['archive_sha256']:
            raise ValueError('image archive hash mismatch')
        with (args.directory / 'import.log').open('wb') as output:
            subprocess.run(['docker', 'load', '--input', str(archive)], stdout=output, stderr=subprocess.STDOUT, check=True, timeout=300)
        image = json.loads(subprocess.check_output(['docker', 'image', 'inspect', 'pipelinefortress:hardened']))[0]
        if image['Id'] != data['image_config_id']:
            raise ValueError('imported image config mismatch')
    print(json.dumps(data))


if __name__ == '__main__':
    main()
