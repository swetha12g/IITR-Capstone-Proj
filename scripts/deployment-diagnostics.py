#!/usr/bin/env python3
"""Publish selected owned-lab diagnostics without kubeconfig, env or secret data."""
import json
import os
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[1]
private = root / "reports/private/day2"
public = root / "reports/sanitized/day2"
public.mkdir(parents=True, exist_ok=True)
text = (private / "deployment.log").read_text(errors="replace")
# Deployment helper output is cluster-control messages, not application responses.
# Exclude creation's exported log paths and any unrelated output by allowlisting.
markers = ["ERROR:", "error:", "failed", "Failed", "timed out", "deadline", "Waiting for", "condition met", " successfully", "Ensuring node image", "Preparing nodes", "Starting control-plane", "Installing", "Joining", "Set kubectl", "kubelet", "cgroup", "swap", "no space", "permission", "containerd"]
lines = [line for line in text.splitlines() if any(marker in line for marker in markers)]
summary = {"deployment_passed": False, "control_messages": lines[-30:], "probes": {}}
env = os.environ.copy()
env["KUBECONFIG"] = str(private / "kubeconfig")
commands = {
    "docker_disk": ["docker", "system", "df"],
    "runner_disk": ["df", "-h", str(root)],
    "kubelet": ["docker", "exec", "pipelinefortress-control-plane", "journalctl", "-u", "kubelet", "--no-pager", "-n", "80"],
    "nodes": ["kubectl", "--context", "kind-pipelinefortress", "get", "nodes"],
    "pods": ["kubectl", "--context", "kind-pipelinefortress", "-n", "pipelinefortress", "get", "pods", "-o", "wide"],
    "events": ["kubectl", "--context", "kind-pipelinefortress", "-n", "pipelinefortress", "get", "events", "--field-selector", "type=Warning", "-o", "json"],
}
for name, command in commands.items():
    try:
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=20)
        if name == "events" and result.returncode == 0:
            output = [{"reason": e.get("reason"), "message": e.get("message"),
                       "object": e.get("involvedObject", {}).get("name")}
                      for e in json.loads(result.stdout).get("items", [])]
        elif name == "kubelet":
            output = [line for line in result.stdout.splitlines() if any(marker in line for marker in markers)][-30:]
        else:
            output = result.stdout[-8000:]
        summary["probes"][name] = {"exit_code": result.returncode, "output": output}
    except subprocess.TimeoutExpired:
        summary["probes"][name] = {"exit_code": 124, "output": "Diagnostic timed out"}
def redact(value):
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        value = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[redacted-contact]", value)
        value = re.sub(r"(https?://)[^/\s:@]+:[^/\s@]+@", r"\1[redacted-auth]@", value)
        value = re.sub(r"(?i)(bearer\s+)[^\s]+", r"\1[redacted]", value)
        value = re.sub(r"\b(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)\b", "[redacted-token]", value)
    return value

summary = redact(summary)
(public / "deployment-failure.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
