# Day 2 checkpoint — complete with recorded incident limitation

Completed on **17 October 2026 (Asia/Kolkata)**, brought forward from the board originally planned for 18 October. All execution-guide Day 2 acceptance checks passed. Days 3–10 and the complete capstone submission remain pending.

## Verified acceptance

- [x] Environment/branch rechecked; authenticated fetch passed and local work preserved.
- [x] Baseline image built from the pinned Juice Shop v20.3.0 source using its original Dockerfile.
- [x] Owned kind/Kubernetes 1.37.0 node and Juice Shop deployment Ready; manifests passed Kubernetes server dry-run.
- [x] Loopback HTTP 200 and sanitized running-app screenshot captured and reviewed.
- [x] Three runtime observations confirmed and documented in [runtime-baseline.md](runtime-baseline.md).
- [x] Hosted application build/tests, source-image build, own-cluster deployment and runtime checks passed.
- [x] Actual CI run/evidence reviewed; Markdown and JIRA checklist closeout prepared for the feature branch.

Local image config: `sha256:79543af23e212f5def487f4daa27763943170f7bb268c46d0aace37920d7ae88`. Linux/amd64, Node v24.22.0, user 65532, port 3000. The local Ready pod's CRI reference resolves to this config ID; zero restarts were observed. See [local runtime evidence](../reports/sanitized/day2/runtime-baseline.json) and [cross-check](../reports/sanitized/day2/local-crosscheck.json).

The designated project-owner reviewer explicitly accepted the local runtime report and screenshot. Hosted CI was still pending at that confirmation; no human approval of its eventual result or independent PR approval is implied.

## Hosted verification

[Successful run 38957969793](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38957969793), job `117165524668`, verified code commit `280514f7bd4f58c9d4e93008f30e9bc4eb72bc90`. Run completed **17 October, 01:33 IST** (16 October, 20:03 UTC).

- All six selected install/build/frontend/server/API stages exited 0; dependency locks unchanged.
- Official kind/kubectl checksum verification and early runner kind-startup check passed.
- Source image build, manifest application, node/pod readiness and exact running-image comparison passed.
- Home, directory listing and metrics returned 200; malformed-search disclosure returned the expected observed 500. All four checker predicates passed.
- Sanitized artifact upload and ephemeral runner-cluster cleanup succeeded.

CI image config: `sha256:4f89b7753b33075d6d158fb22f711e7707881d0a29edb2c3183a2064c0e5676c`. This is the runner's own image, separate from the laptop image. Artifact `12071418832` SHA-256 matched `fd1c109c1eddfcd13708fa0955d4a9a1f16e3a990ce79645acd5ffba19633f42` after download. Durable records: [CI receipt](../reports/sanitized/day2/ci-receipt.json), [build/tests](../reports/sanitized/day2/ci/build-tests.json), [runtime](../reports/sanitized/day2/ci/runtime-baseline.json).

## Earlier failed job and investigation limit

[Run 38955433523, job 117157402202](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38955433523/job/117157402202) passed tests/image build but deployment exited 1. Its private deployment log was discarded with the runner; the available artifact contained only the passing test manifest. **Its exact root cause remains unconfirmed.** The current successful run proves current acceptance, not the historical cause. No timeout increase or skipped gate was used to obtain success.

The workflow now checks kind startup before expensive builds, retains a failed owned node until diagnostics finish, publishes selected/redacted operational diagnostics on failure, and cleans up afterward. Synthetic contact/auth/token redaction checks passed. Kubeconfig contents, environment dumps, secret resources, raw application responses and raw private logs are excluded. Investigation status: **DONE_WITH_CONCERNS** for workflow recovery and evidence; historical root cause cannot be recovered from the retained first-run evidence.

## Reproduce and access

```bash
source scripts/dev-env.sh
python scripts/run-day1-checks.py
bash scripts/build-image.sh
bash scripts/deploy.sh
python scripts/runtime-baseline.py
```

The deployment helper uses a dedicated ignored kubeconfig and loads the built image. Its pod-template image-config-ID annotation triggers a rollout when that image changes. A local rollout and subsequent unchanged-image apply passed, followed by another runtime identity check. The checker opens/closes its own loopback forward; interactive access and explicit lab-removal commands are in [runtime-baseline.md](runtime-baseline.md#reproduce-and-access). The local cluster is retained, with no port-forward left running by this session.

The kind node is digest-pinned from the [official 0.33.0 release](https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0). Action SHAs and runner/runtime pins are in [security.yml](../.github/workflows/security.yml) and [versions.md](versions.md). No persistent bridge, shell startup or system Node changes were added.

## Limits and next step

The original Dockerfile retains mutable base tags/tool ranges; exact observed images are recorded and identical rebuild digests are not promised. Eight upstream Day 1 test skips remain; Cypress E2E is not claimed. Security scanners/gates, hardening, AI safeguards/evaluation, remediation PRs and the rendered 12-page report remain pending. Submission cutoff and coordinator/independent-review interpretation remain open external facts.

Stop at Day 2. The next unstarted checkpoint is the [Day 3 JIRA backlog](daily-log.md#next-checkpoint-backlog--day-3-planned-for-18-october-2026). Day 4 acknowledgement and later live-AI budget/model decisions remain separate prerequisites.

Operational learning: a changed local image tag requires a deployment-template change to replace old pods; private runner logs need selected diagnostic artifacts before cleanup if future root-cause analysis is to remain possible.
