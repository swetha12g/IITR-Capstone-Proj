#!/usr/bin/env python3
"""Capture non-destructive baseline checks against this runner's owned kind lab."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "reports/private/day2"
PUBLIC = ROOT / "reports/sanitized/day2"
ENV = os.environ.copy()
ENV["KUBECONFIG"] = str(Path(ENV.get("PIPELINEFORTRESS_KUBECONFIG", ENV.get(
    "KUBECONFIG", str(PRIVATE / "kubeconfig")))).resolve())
KUBE = ["kubectl", "--context", "kind-pipelinefortress"]
APP = KUBE + ["-n", "pipelinefortress"]
HTTP = build_opener(ProxyHandler({}))


def data(command):
    return json.loads(subprocess.check_output(command, env=ENV, timeout=30))


def request(path):
    try:
        response = HTTP.open("http://127.0.0.1:3000" + path, timeout=10)
    except HTTPError as error:
        response = error
    with response:
        return response.status, response.read(4 * 1024 * 1024)


def main():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    image = data(["docker", "image", "inspect", "pipelinefortress:baseline"])[0]
    nodes = data(KUBE + ["get", "nodes", "-o", "json"])["items"]
    pods = data(APP + ["get", "pods", "-l", "app.kubernetes.io/name=juice-shop", "-o", "json"])["items"]
    service = data(APP + ["get", "service", "juice-shop", "-o", "json"])
    assert nodes and all(any(c["type"] == "Ready" and c["status"] == "True"
                            for c in n["status"]["conditions"]) for n in nodes)
    assert pods and all(any(c["type"] == "Ready" and c["status"] == "True"
                           for c in p["status"]["conditions"]) for p in pods)
    assert service["spec"]["type"] == "ClusterIP"
    manifest = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "owned kind-pipelinefortress lab; loopback HTTP only; no login or mutating HTTP methods",
        "source_commit": "f189f521266f42c6bd05884468292000cee852ed",
        "image": {"id": image["Id"], "architecture": image["Architecture"],
                  "os": image["Os"], "user": image["Config"]["User"],
                  "ports": sorted(image["Config"].get("ExposedPorts", {}))},
        "nodes": [{"name": n["metadata"]["name"], "ready": True,
                   "kubelet": n["status"]["nodeInfo"]["kubeletVersion"]} for n in nodes],
        "pods": [{"name": p["metadata"]["name"], "ready": True,
                  "containers": [{"image": c["image"], "image_id": c["imageID"],
                                  "restarts": c["restartCount"]}
                                 for c in p["status"]["containerStatuses"]]} for p in pods],
        "service_type": service["spec"]["type"], "checks": [],
    }
    for raw_pod, pod in zip(pods, manifest["pods"]):
        node_name = raw_pod["spec"]["nodeName"]
        assert node_name == "pipelinefortress-control-plane"
        for container in pod["containers"]:
            # CRI reports a manifest digest; Docker's image ID is its config digest.
            # Resolve the exact running CRI reference before comparing config IDs.
            inspected = data(["docker", "exec", node_name, "crictl", "inspecti", "docker.io/library/pipelinefortress:baseline"])
            container["config_id"] = inspected["status"]["id"]
            assert container["image_id"] in inspected["status"]["repoDigests"], "Running digest differs from the imported image"
            assert container["config_id"] == image["Id"], "Pod is not running the built image"
    with (PRIVATE / "port-forward.log").open("wb") as output:
        forward = subprocess.Popen(APP + ["port-forward", "--address", "127.0.0.1",
                                          "service/juice-shop", "3000:3000"],
                                   stdout=output, stderr=subprocess.STDOUT, env=ENV)
        try:
            for attempt in range(60):
                assert forward.poll() is None, "Owned port-forward exited; inspect its private log"
                if b"Forwarding from 127.0.0.1:3000" in (PRIVATE / "port-forward.log").read_bytes():
                    try:
                        status, body = request("/")
                        if status == 200:
                            break
                    except (URLError, TimeoutError):
                        pass
                time.sleep(1)
            else:
                raise RuntimeError("Loopback HTTP did not become ready")
            checks = [
                ("http-home", "/", lambda s, b: s == 200 and b"<html" in b.lower()),
                ("unauthenticated-directory-listing", "/ftp/", lambda s, b: s == 200 and b"acquisitions.md" in b),
                ("unauthenticated-metrics", "/metrics", lambda s, b: s == 200 and b"# HELP" in b and b"process_" in b),
                ("sql-error-disclosure", "/rest/products/search?q=%27%29", lambda s, b: s == 500 and b"SQLITE_ERROR" in b and b"stack" in b),
            ]
            for identifier, path, predicate in checks:
                status, body = request(path)
                filename = PRIVATE / (identifier + ".response")
                filename.write_bytes(body)
                manifest["checks"].append({"id": identifier, "method": "GET", "path": path,
                    "http_status": status, "confirmed": bool(predicate(status, body)),
                    "response_bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                    "private_evidence": str(filename.relative_to(ROOT))})
        finally:
            forward.terminate()
            try:
                forward.wait(timeout=10)
            except subprocess.TimeoutExpired:
                forward.kill()
                forward.wait(timeout=10)
    manifest["passed"] = all(c["confirmed"] for c in manifest["checks"])
    (PUBLIC / "runtime-baseline.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"passed": manifest["passed"], "checks": manifest["checks"]}, indent=2))
    return 0 if manifest["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
