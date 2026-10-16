# Day 2 checkpoint — source image, kind lab and baseline CI

Started on **17 October 2026 (Asia/Kolkata)** at the user's request, bringing forward the board originally planned for 18 October. This records the execution guide's Day 2 only; Days 3–10 and the full submission remain pending.

## Verified so far

- Preserved the clean Day 1 delivery on `feature-16-kick-start`; authenticated fetch succeeded.
- Rechecked Docker 27.3.1, kind 0.33.0, kubectl 1.37.0, project Node 24.22.0/npm 11.19.1 and Python dependency health. Docker reported no warnings. Bridge filters and IPv4 forwarding remain enabled.
- Built `pipelinefortress:baseline` from the exact imported Juice Shop v20.3.0 source using its upstream Dockerfile; build exited 0. The pinned Kubernetes node image was downloaded successfully.
- Authored one-node kind configuration, namespace, deployment and ClusterIP service; no public ingress. Kubernetes server dry-run passed; node and workload are Ready.
- Authored and validated a SHA-pinned baseline Actions workflow. Implementation commit `f9867e0` was pushed normally. [Hosted run 38954124002](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38954124002) is in progress; CI is not yet marked passed.

## Execution contract

`scripts/build-image.sh` uses the recorded dependency locks and original Dockerfile. `scripts/deploy.sh` uses a dedicated ignored kubeconfig under `reports/private/day2/`, loads the built image, validates manifests against the API, annotates the pod template with the exact image config ID and waits for readiness. Rebuilding the local tag therefore triggers a rollout rather than leaving an old pod running. `scripts/runtime-baseline.py` owns a temporary loopback port-forward and records only safe status/identifiers/hashes. Raw responses and logs remain ignored.

The kind node digest comes from the [official kind 0.33.0 release](https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0): Kubernetes 1.37.0, matching the installed kubectl client. The hosted workflow creates and deletes its own cluster; it does not contact the laptop cluster.

## Open acceptance

- [x] Source image built.
- [x] Local kind node and workload Ready.
- [x] Loopback HTTP and sanitized screenshot captured; [capture metadata](../reports/sanitized/day2/screenshot.json).
- [x] Three runtime observations confirmed and documented in [runtime-baseline.md](runtime-baseline.md).
- [ ] Hosted baseline build/test/deployment succeeds; run URL recorded.
- [ ] Final evidence/checklists reviewed and published.

Submission cutoff time and coordinator interpretation of independent review remain unconfirmed. The project owner is the designated manual reviewer; this document does not invent a human approval.

## Manual review and delivery

The designated project-owner reviewer explicitly confirmed review and acceptance of the **local** Day 2 evidence on 17 October. Hosted CI was pending at that confirmation, so no human review of its eventual result is implied. This records real local manual review, not independent PR approval. Implementation `f9867e0` was pushed to the requested feature branch to execute the agreed workflow; final documentation delivery follows the hosted result.

## Reproduce and stop

From repository root, select the project environment and run:

```bash
source scripts/dev-env.sh
python scripts/run-day1-checks.py
bash scripts/build-image.sh
bash scripts/deploy.sh
python scripts/runtime-baseline.py
```

The checker closes its temporary forward; the local cluster remains available for the next stage. Interactive access and explicit lab removal commands are in [runtime-baseline.md](runtime-baseline.md#reproduce-and-access). Hosted CI cleans up its own cluster in an always-run finalization step. Keep the kubeconfig and raw logs private.

## Remaining limits and next step

The upstream Dockerfile is retained for baseline evidence, including mutable base tags/tool ranges. The exact observed image is recorded; identical rebuild digests are not promised. The finite application suites retain eight upstream skips and do not cover Cypress E2E. No security scanners, AI calls, remediation PRs or final report are completed by Day 2.

Next is the guide's Day 3: pinned Semgrep, dependency and secrets scanning with bad/fixed gates, failure handling and sanitized evidence. Day 4 acknowledgement and later AI budget/model decisions remain separate prerequisites; no later-stage work is started here.

### Deployment rerun correction

Final reproduction review identified that changing a local image tag does not itself replace existing pods. The deployment helper now writes the built image config ID into the pod template annotation, so changed images trigger a rollout and unchanged images remain stable. Local validation/rerun is being checked. The first hosted run passed build/tests; its final image/deployment result is superseded by the new verification run after this helper correction.
