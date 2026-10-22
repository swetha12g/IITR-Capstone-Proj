#!/usr/bin/env bash
set -euo pipefail
pipelinefortress_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$pipelinefortress_root"
mkdir -p reports/private/reproduction
python3 scripts/bootstrap-project.py > reports/private/reproduction/bootstrap.log 2>&1
source scripts/dev-env.sh
export PATH="$pipelinefortress_root/.tools/ci/pipelinefortress-tools:$PATH"
export PIPELINEFORTRESS_NODE_DIR="$pipelinefortress_root/.tools/node/node-v24.22.0-linux-x64"
source scripts/dev-env.sh
docker info > reports/private/reproduction/docker-info.log 2>&1
python scripts/install-scanners.py > reports/private/reproduction/source-tools.log 2>&1
python scripts/install-day4-tools.py > reports/private/reproduction/day4-tools.log 2>&1
python -m pytest tests/triage tests/redaction -q > reports/private/reproduction/contracts.log 2>&1
python scripts/verify-day4-policies.py > reports/private/reproduction/policy-fixtures.log 2>&1

# A unique owned cluster avoids relying on or deleting the original study lab.
export PIPELINEFORTRESS_CLUSTER="pipelinefortress-repro-$$"
export PIPELINEFORTRESS_KUBECONFIG="$pipelinefortress_root/reports/private/reproduction/kubeconfig"
pipelinefortress_created=0
pipelinefortress_cleanup() {
  local pipelinefortress_result=$?
  if [[ "$pipelinefortress_created" == 1 ]]; then
    kind delete cluster --name "$PIPELINEFORTRESS_CLUSTER" --kubeconfig "$PIPELINEFORTRESS_KUBECONFIG" \
      >> reports/private/reproduction/cleanup.log 2>&1 || pipelinefortress_result=2
  fi
  python - "$pipelinefortress_result" <<'PY'
from pathlib import Path
import json,os,subprocess,sys
path=Path('reports/sanitized/reproduction/run.json')
receipt=json.loads(path.read_text()) if path.is_file() else {'verdict':'ERROR','scope':'fresh directory reproduction'}
nodes=subprocess.check_output(['docker','ps','-a','--filter','label=io.x-k8s.kind.cluster='+os.environ['PIPELINEFORTRESS_CLUSTER'],'--format','{{.ID}}']).decode().strip()
receipt['cleanup_verified']=not bool(nodes)
receipt['script_exit_code']=int(sys.argv[1])
if nodes or int(sys.argv[1]):receipt['verdict']='ERROR'
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(receipt,indent=2)+'\n')
PY
  return "$pipelinefortress_result"
}
trap pipelinefortress_cleanup EXIT
pipelinefortress_created=1
kind create cluster --name "$PIPELINEFORTRESS_CLUSTER" --config infra/kind.yaml \
  --kubeconfig "$PIPELINEFORTRESS_KUBECONFIG" --wait 180s --retain > reports/private/reproduction/cluster.log 2>&1
python scripts/run-study-pipeline.py > reports/private/reproduction/pipeline.log 2>&1
python -m triage.normalize --input-dir reports/private --output reports/private/normalized.json
python -m triage.client --input reports/private/normalized.json --output reports/private/reproduction/mock-triage.json --dry-run --limit 20
python scripts/build-deferred-register.py
python metrics/build_dashboard.py --findings reports/private/normalized.json --labels metrics/labels.json --output reports/sanitized/dashboard/index.html
python - <<'PY'
from pathlib import Path
import json,os,subprocess
aggregate=json.loads(Path('reports/sanitized/pipeline/aggregate.json').read_text())
receipt={'scope':'fresh directory, project-local bootstrap, unique ephemeral owned cluster, no live API',
         'verdict':aggregate['verdict'],'run_id':aggregate['run_id'],'operational_errors':aggregate['operational_errors'],
         'application_profile':'offline-local; external service availability suite excluded',
         'cleanup':'handled by shell finalization; verify cleanup.log and cluster inventory',
         'project_commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()}
Path('reports/sanitized/reproduction/run.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
PY
