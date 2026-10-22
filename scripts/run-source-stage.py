#!/usr/bin/env python3
"""One CI source-scan job; actual finding exits remain valid study evidence."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['sast', 'sca', 'secrets'], required=True)
    args = parser.parse_args()
    started = time.monotonic()
    private = ROOT / 'reports/private/pipeline' / (args.stage + '-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    private.mkdir(parents=True)
    env = scans.tool_environment(private)
    if args.stage == 'secrets':
        if subprocess.check_output(['git', 'rev-parse', '--is-shallow-repository'], cwd=ROOT).strip() != b'false':
            raise ValueError('full history is required')
        scans.snapshot(private / 'working-tree')
    selected = {'secrets-history', 'secrets-tree'} if args.stage == 'secrets' else {args.stage}
    reports = []
    for stage, command, finding_code in scans.commands(private, ROOT / 'app/juice-shop', ROOT):
        if stage not in selected:
            continue
        if stage == 'sca':
            for origin, destination in [('package-lock.json', 'package-lock.json'), ('frontend-package-lock.json', 'frontend/package-lock.json')]:
                if (ROOT / 'locks/juice-shop' / origin).read_bytes() != (ROOT / 'app/juice-shop' / destination).read_bytes():
                    raise ValueError('application lock differs from retained pin')
        entry = scans.collect(stage, command, private / (stage + '.json'), private, env, finding_code)
        if entry['execution'] == 'error':
            raise RuntimeError('scanner execution failed')
        reports.append((stage, private / (stage + '.json'), entry['exit_code']))
    receipt = publish(args.stage, reports, duration_seconds=round(time.monotonic() - started, 2))
    print(json.dumps({'stage': args.stage, 'execution': receipt['execution'], 'findings': receipt['findings_by_severity']}))


if __name__ == '__main__':
    main()
