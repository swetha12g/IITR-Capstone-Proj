#!/usr/bin/env bash
set -euo pipefail
pipelinefortress_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$pipelinefortress_root"
export KUBECONFIG="${PIPELINEFORTRESS_KUBECONFIG:-$pipelinefortress_root/reports/private/day2/kubeconfig}"
mkdir -p "$(dirname -- "$KUBECONFIG")"
if [[ " $(kind get clusters | tr '\n' ' ') " != *" pipelinefortress "* ]]; then
  KIND_EXPERIMENTAL_PROVIDER=docker kind create cluster --name pipelinefortress \
    --config infra/kind.yaml --kubeconfig "$KUBECONFIG" --wait 180s
fi
kubectl --context kind-pipelinefortress wait --for=condition=Ready nodes --all --timeout=180s
kind load docker-image pipelinefortress:baseline --name pipelinefortress
kubectl --context kind-pipelinefortress apply --dry-run=client --validate=strict -f infra/k8s/namespace.yaml
kubectl --context kind-pipelinefortress apply -f infra/k8s/namespace.yaml
kubectl --context kind-pipelinefortress apply --dry-run=server -f infra/k8s/
kubectl --context kind-pipelinefortress apply -f infra/k8s/
kubectl --context kind-pipelinefortress -n pipelinefortress rollout status deployment/juice-shop --timeout=300s
kubectl --context kind-pipelinefortress -n pipelinefortress wait --for=condition=Ready pods \
  -l app.kubernetes.io/name=juice-shop --timeout=180s
