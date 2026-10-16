#!/usr/bin/env bash
set -euo pipefail
pipelinefortress_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$pipelinefortress_root"
cp locks/juice-shop/package-lock.json app/juice-shop/package-lock.json
cp locks/juice-shop/frontend-package-lock.json app/juice-shop/frontend/package-lock.json
docker build --progress=plain \
  --build-arg VCS_REF=f189f521266f42c6bd05884468292000cee852ed \
  --build-arg "BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -t pipelinefortress:baseline app/juice-shop
