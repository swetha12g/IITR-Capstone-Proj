#!/usr/bin/env bash
set -euo pipefail
pipelinefortress_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$pipelinefortress_root"
exec python3 scripts/run-scans.py "$@"
