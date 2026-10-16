#!/usr/bin/env bash
set -euo pipefail
pipelinefortress_tools="${RUNNER_TEMP:?This installer is for the ephemeral CI runner}/pipelinefortress-tools"
mkdir -p "$pipelinefortress_tools"
curl --fail --silent --show-error --location --connect-timeout 20 --max-time 180 --retry 2 \
  https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64 \
  --output "$pipelinefortress_tools/kind-linux-amd64"
curl --fail --silent --show-error --location --connect-timeout 20 --max-time 180 --retry 2 \
  https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64.sha256sum \
  --output "$pipelinefortress_tools/kind-linux-amd64.sha256sum"
(cd "$pipelinefortress_tools" && sha256sum --check kind-linux-amd64.sha256sum)
curl --fail --silent --show-error --location --connect-timeout 20 --max-time 180 --retry 2 \
  https://dl.k8s.io/release/v1.37.0/bin/linux/amd64/kubectl \
  --output "$pipelinefortress_tools/kubectl"
curl --fail --silent --show-error --location --connect-timeout 20 --max-time 180 --retry 2 \
  https://dl.k8s.io/release/v1.37.0/bin/linux/amd64/kubectl.sha256 \
  --output "$pipelinefortress_tools/kubectl.sha256"
python3 - "$pipelinefortress_tools" <<'PY'
import hashlib
from pathlib import Path
import re
import sys
root = Path(sys.argv[1])
expected = (root / "kubectl.sha256").read_text().strip()
assert re.fullmatch(r"[a-fA-F0-9]{64}", expected)
assert hashlib.sha256((root / "kubectl").read_bytes()).hexdigest() == expected.lower()
print("kubectl official checksum: passed")
PY
install -m 0755 "$pipelinefortress_tools/kind-linux-amd64" "$pipelinefortress_tools/kind"
chmod 0755 "$pipelinefortress_tools/kubectl"
printf '%s\n' "$pipelinefortress_tools" >> "${GITHUB_PATH:?}"
