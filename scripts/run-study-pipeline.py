#!/usr/bin/env python3
"""Execute the complete local study workflow, preserving every command outcome."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from triage.evidence import aggregate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-build', action='store_true', help='Use the current verified six-step build/test and exact image; record reuse explicitly')
    args = parser.parse_args()
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    private = ROOT / 'reports/private/pipeline' / ('run-' + run_id)
    private.mkdir(parents=True)
    env = os.environ.copy()
    env['PIPELINEFORTRESS_RUN_ID'] = run_id
    manifest = {'schema_version': 1, 'run_id': run_id, 'started_at_utc': datetime.now(timezone.utc).isoformat(),
                'build_test_reused': args.reuse_build, 'steps': []}
    before = time.monotonic()
    commands = []
    if not args.reuse_build:
        commands += [('application', ['scripts/run-day1-checks.py', '--offline']), ('build-image', ['scripts/build-hardened-image.py'])]
    commands += [('build-test', ['scripts/run-artifact-stage.py', '--stage', 'build-test'])]
    commands += [(s, ['scripts/run-source-stage.py', '--stage', s]) for s in ['sast', 'sca', 'secrets']]
    commands += [(s, ['scripts/run-artifact-stage.py', '--stage', s]) for s in ['iac', 'container']]
    commands += [('deploy', ['scripts/deploy-hardened.py']), ('runtime', ['scripts/verify-hardened-runtime.py', '--mode', 'kubernetes']),
                 ('zap', ['scripts/run-dast.py']), ('dast', ['scripts/run-artifact-stage.py', '--stage', 'dast'])]
    failure = False
    for label, arguments in commands:
        started = time.monotonic()
        with (private / (label + '.log')).open('wb') as log:
            try:
                result = subprocess.run([sys.executable, *arguments], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1800)
                code = result.returncode
            except (OSError, subprocess.TimeoutExpired):
                code = 124
        manifest['steps'].append({'step': label, 'exit_code': code, 'duration_seconds': round(time.monotonic() - started, 2)})
        (private / 'execution.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(json.dumps(manifest['steps'][-1]), flush=True)
        if code:
            failure = True
            if label in {'application', 'build-image', 'build-test', 'deploy'}:
                break
    receipts = ROOT / 'reports/sanitized/pipeline'
    result = aggregate(receipts)
    result['run_id'] = run_id
    result['duration_seconds'] = round(time.monotonic() - before, 2)
    result['build_test_reused'] = args.reuse_build
    result['execution_steps'] = manifest['steps']
    if failure:
        result['verdict'] = 'ERROR'
        result['operational_errors'].append('local-command-failed')
    (receipts / 'aggregate.json').write_text(json.dumps(result, indent=2) + '\n')
    if not result['operational_errors']:
        index = []
        for stage in ['sast', 'sca', 'secrets', 'iac', 'container', 'dast']:
            metadata = json.loads((ROOT / 'reports/private/pipeline' / ('latest-' + stage + '.json')).read_text())
            if metadata['run_id'] != run_id:
                raise ValueError('normalization index has mixed runs')
            for report in metadata['reports']:
                index.append({**report, **{k: metadata[k] for k in ['run_id', 'commit', 'observed_at_utc']}})
        (ROOT / 'reports/private/pipeline/latest-index.json').write_text(json.dumps({'run_id': run_id, 'reports': index}, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['verdict', 'run_id', 'operational_errors', 'deferred_observations']}))
    return 2 if result['operational_errors'] else 1 if result['security_blockers'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
