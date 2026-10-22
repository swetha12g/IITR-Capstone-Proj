#!/usr/bin/env python3
"""Fail on critical findings or execution errors; retain deferred lower severities."""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from triage.evidence import aggregate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipts', type=Path, default=ROOT / 'reports/sanitized/pipeline')
    parser.add_argument('--output', type=Path, default=ROOT / 'reports/sanitized/pipeline/aggregate.json')
    args = parser.parse_args()
    needs = json.loads(os.environ['PIPELINEFORTRESS_JOB_RESULTS']) if 'PIPELINEFORTRESS_JOB_RESULTS' in os.environ else None
    result = aggregate(args.receipts, needs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['verdict', 'stage_count', 'deferred_observations', 'operational_errors']}))
    return 2 if result['operational_errors'] else 1 if result['security_blockers'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
