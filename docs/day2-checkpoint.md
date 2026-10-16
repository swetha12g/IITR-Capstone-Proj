# Day 2 checkpoint — source image, kind lab and baseline CI

Started on **17 October 2026 (Asia/Kolkata)** at the user's request, bringing forward the board originally planned for 18 October. This records the execution guide's Day 2 only; Days 3–10 and the full submission remain pending.

## Verified so far

- Preserved the clean Day 1 delivery on `feature-16-kick-start`; authenticated fetch succeeded.
- Rechecked Docker 27.3.1, kind 0.33.0, kubectl 1.37.0, project Node 24.22.0/npm 11.19.1 and Python dependency health. Docker reported no warnings. Bridge filters and IPv4 forwarding remain enabled.
- Built `pipelinefortress:baseline` from the exact imported Juice Shop v20.3.0 source using its upstream Dockerfile; build exited 0. The pinned Kubernetes node image was downloaded successfully.
- Authored one-node kind configuration, namespace, deployment and ClusterIP service; no public ingress. Kubernetes server dry-run passed; node and workload are Ready.
- Authored a SHA-pinned baseline Actions workflow. An actual hosted run is still required before CI acceptance can be marked complete.

## Execution contract

`scripts/build-image.sh` uses the recorded dependency locks and original Dockerfile. `scripts/deploy.sh` uses a dedicated ignored kubeconfig under `reports/private/day2/`, loads the built image, validates manifests against the API and waits for readiness. `scripts/runtime-baseline.py` owns a temporary loopback port-forward and records only safe status/identifiers/hashes. Raw responses and logs remain ignored.

The kind node digest comes from the [official kind 0.33.0 release](https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0): Kubernetes 1.37.0, matching the installed kubectl client. The hosted workflow creates and deletes its own cluster; it does not contact the laptop cluster.

## Open acceptance

- [x] Source image built.
- [x] Local kind node and workload Ready.
- [ ] Loopback HTTP and sanitized screenshot captured.
- [x] Three runtime observations confirmed and documented in [runtime-baseline.md](runtime-baseline.md).
- [ ] Hosted baseline build/test/deployment succeeds; run URL recorded.
- [ ] Final evidence/checklists reviewed and published.

Submission cutoff time and coordinator interpretation of independent review remain unconfirmed. The project owner is the designated manual reviewer; this document does not invent a human approval.
