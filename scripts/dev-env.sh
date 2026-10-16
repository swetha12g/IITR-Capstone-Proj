#!/usr/bin/env bash
# Source this file to select the project's user-local Node and Python runtimes.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  printf '%s\n' 'Run: source scripts/dev-env.sh'
  exit 1
fi

pipelinefortress_repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
pipelinefortress_node_dir="${PIPELINEFORTRESS_NODE_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/pipelinefortress/node-v24.22.0-linux-x64}"

if [[ ! -x "$pipelinefortress_node_dir/bin/node" ]]; then
  printf '%s\n' 'Project Node runtime is missing; see docs/versions.md.' >&2
  unset pipelinefortress_repo_dir pipelinefortress_node_dir
  return 1
fi

if [[ -f "$pipelinefortress_repo_dir/.venv/bin/activate" ]]; then
  source "$pipelinefortress_repo_dir/.venv/bin/activate"
fi

export PATH="$pipelinefortress_node_dir/bin:$PATH"
hash -r
unset pipelinefortress_repo_dir pipelinefortress_node_dir
