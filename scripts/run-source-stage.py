#!/usr/bin/env python3
"""One CI source-scan job; actual finding exits remain valid study evidence."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from triage.evidence import publish

spec = importlib.util.spec_from_file_location('source_scans', ROOT / 'scripts/run-scans.py')
scans = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scans)


def prepare_locks(root):
    for origin, destination in [('package-lock.json', 'package-lock.json'), ('frontend-package-lock.json', 'frontend/package-lock.json')]:
        source = root / 'locks/juice-shop' / origin
        target = root / 'app/juice-shop' / destination
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError('application lock differs from retained pin; local file preserved')
        if not target.exists():
            shutil.copyfile(source, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['sast', 'sca', 'secrets'], required=True)
    args = parser.parse_args()
    started = time.monotonic()
    private = ROOT / 'reports/private/pipeline' / (args.stage + '-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    private.mkdir(parents=True)
    (ROOT / 'reports/sanitized/pipeline' / (args.stage + '.json')).unlink(missing_ok=True)
    env = scans.tool_environment(private)
    if args.stage == 'sca':
        prepare_locks(ROOT)
    if args.stage == 'secrets':
        if subprocess.check_output(['git', 'rev-parse', '--is-shallow-repository'], cwd=ROOT).strip() != b'false':
            raise ValueError('full history is required')
        scans.snapshot(private / 'working-tree')
    selected = {'secrets-history', 'secrets-tree'} if args.stage == 'secrets' else {args.stage}
    reports = []
    for stage, command, finding_code in scans.commands(private, ROOT / 'app/juice-shop', ROOT):
        if stage not in selected:
            continue
        entry = scans.collect(stage, command, private / (stage + '.json'), private, env, finding_code)
        if entry['execution'] == 'error':
            raise RuntimeError('scanner execution failed')
        reports.append((stage, private / (stage + '.json'), entry['exit_code']))
        if stage == 'sast':
            data = json.loads((private / 'sast.json').read_text())
            # Classify incomplete scans without publishing paths/messages/code.
            error_types = []
            for error in data.get('errors', []):
                category = error.get('type', '') if isinstance(error, dict) else ''
                error_types.append(category if isinstance(category, str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,70}', category) else 'unclassified')
            print(json.dumps({'stage': 'sast', 'scanned_files': len(data.get('paths', {}).get('scanned', [])),
                              'finding_count': len(data.get('results', [])), 'error_types': error_types}), flush=True)
    receipt = publish(args.stage, reports, duration_seconds=round(time.monotonic() - started, 2))
    print(json.dumps({'stage': args.stage, 'execution': receipt['execution'], 'findings': receipt['findings_by_severity']}))


if __name__ == '__main__':
    main()
