# Day 4 checkpoint — updated 22 October 2026

**Historical comparison:** The counts below describe the original hardening stage before the later critical-remediation request. Current source/image scans have zero critical findings; current runtime/build receipts refer to the remediated image. The frozen Day 4 comparison remains historical. See [critical remediation](critical-remediation.md).

**Current status: hardening verified locally; vulnerabilities deferred for continued study execution.** Days 1–3 have historical local/hosted evidence. On 22 October the user confirmed signing the Responsible AI acknowledgement and explicitly requested resumption, clearing the entry condition in the [execution guide](../10-days-work-break-down.md#day-4--iac-secure-image-and-sbom). Actual signing date was not supplied; no signature or signed record is stored here. The historical strict gate identifies 39 residual findings. The later user-directed study profile passes execution while deferring these findings; operational errors remain errors. See [current completion state](project-completion.md) for Days 5–10.

## Historical preflight — 19 October

| Check | Result on 19 October |
|---|---|
| Repository | Clean at entry, branch `feature-16-kick-start`, HEAD `993f1df`; matched the existing remote-tracking ref (`0 / 0`), without fetching or publishing |
| Project runtimes | Node v24.22.0, npm 11.19.1, Python 3.10.12; Python dependency check passed |
| Application locks | Both working copies match the retained project locks |
| Docker | Server 27.3.1 reachable; existing baseline image present, amd64, configured user 65532 |
| Baseline image identity | Docker image/config ID `sha256:79543af23e212f5def487f4daa27763943170f7bb268c46d0aace37920d7ae88`; not a registry manifest digest |
| Existing owned lab | Kubernetes v1.37.0 node Ready; `juice-shop` deployment has one ready replica out of one desired, using `pipelinefortress:baseline` |
| Available disk | Approximately 570 GiB free |
| Day 4 scanners | `checkov` and `syft` not found on the selected project PATH; no installation attempted |
| Temporary bridge settings | IPv4 forwarding is 1; both bridge-filter sysctl paths are absent and Docker reports both disabled. Earlier temporary setup is not assumed to persist. This observation alone does not prove a networking failure |

Those preflight checks were read-only; the work below was performed after the 22 October confirmation.

## Current task state

| ID | Task and acceptance evidence | Current status |
|---|---|---|
| PF-D4-00 | Confirm actual acknowledgement completion/date; keep any signed record private | Complete: user confirmation received 22 October; signing date unspecified |
| PF-D4-01 | Isolate/pin Checkov; run built-in checks and custom immutable-image policy against actual passing/failing fixtures | Verified: Checkov 3.3.30, 100 hash-pinned distributions, eight actual CLI fixtures including init-container and CronJob cases |
| PF-D4-02 | Select a CIS benchmark/version, map applicable controls and document uncovered controls | Verified bounded CIS 2.0.0 mapping; [controls and gaps](day4-controls.md); no full-cluster compliance claim |
| PF-D4-03 | Build a supported, digest-pinned, minimal non-root image; verify required writable paths and application behavior | Verified production build and seven Docker runtime checks; source/locks preserved |
| PF-D4-04 | Test Kubernetes security contexts, disabled service-account token, resources/probes and read-only root with explicit writable mounts in the owned lab | Verified Ready rollout, exact CRI/Docker config match, seven HTTP checks and process/filesystem enforcement checks |
| PF-D4-05 | Pin Syft; scan and inventory the exact hardened image, validate CycloneDX schema/packages and retain image/SBOM/DB identities | Verified Syft 1.55.0, Trivy 0.76.0, 2,748-component CycloneDX 1.6 schema/representative-package validation |
| PF-D4-06 | Compare actual baseline/hardened results and runtime; extend gate/evidence without widening the existing 186 risk approvals | Comparison and 15 gate contracts verified; one IaC and 38 high/critical container findings are deferred under the study profile |

## Measured result

| Measure | Baseline | Hardened |
|---|---:|---:|
| Failed Kubernetes checks | 15 | 1 |
| Failed Dockerfile checks | 2 | 0 |
| Image vulnerability identities | 101 | 100 |
| Critical / high / unknown | 11 / 27 / 1 | 11 / 27 / 0 |
| Image size (bytes) | 351,789,266 | 345,391,667 |
| Same seven functional/training checks | Historical baseline has four checks; no new seven-check baseline run claimed | 7/7 Docker and 7/7 Kubernetes |

Sixteen IaC/Dockerfile failures and one unknown CA-certificate advisory were removed, with no new vulnerability identities. The remaining high/critical application findings were not fixed by runtime hardening. The [residual-risk record](day4-risk-review.md) and [gate summary](../reports/sanitized/day4/gate-summary.json) identify the open acceptance boundary. No Day 4 exception was activated; existing source approvals remain exact and expire on 25 October 2026 at 00:00 IST.

Hardened Docker image/config ID: `sha256:3eb3e0ff60e5fba12f014e5fcc9f6086fa7f366139d52a4bce44e598a3e860e9`. Local kind/containerd manifest digest: `sha256:77f2b09d4c678186e64caafef22ec929a01f4211a1e12d67b28d97e008707549`. These are different identities; the latter was named locally for digest-based deployment and was **not published to a registry**. [Deployment evidence](../reports/sanitized/day4/deployment.json), [Docker controls](../reports/sanitized/day4/runtime-docker.json), [Kubernetes controls](../reports/sanitized/day4/runtime-kubernetes.json), [scan/DB/report hashes](../reports/sanitized/day4/scan-execution.json).

The existing node initially reported Ready while multiple pods were unready and carried future-dated startup timestamps relative to the current host/node clocks. Private diagnostics were retained and only the owned node's kubelet service was restarted; no host sysctl/module, system tool or unrelated container was changed. The new workload now has one Ready replica and zero restarts. Other system pods still have readiness issues; their recovery and the initial cause are not claimed resolved. The initial local import-name mismatch was corrected by registering a canonical digest reference in this lab's containerd and checking both manifest/config identities.

## Reproduce locally

```bash
source scripts/dev-env.sh
export PATH="$HOME/.local/bin:$PATH"
python scripts/install-day4-tools.py
python scripts/verify-day4-policies.py
python scripts/build-hardened-image.py
python scripts/verify-hardened-runtime.py --mode docker
python scripts/deploy-hardened.py
python scripts/verify-hardened-runtime.py --mode kubernetes
python scripts/run-day4-scans.py
python scripts/test-day4-gates.py
python scripts/gate-day4.py --manifest "$(cat reports/private/day4/latest-manifest.txt)"
```

The comparison requires both recorded immutable baseline/hardened Docker images, the pinned Day 3 Trivy binary and the existing owned kind cluster/kubeconfig. The final command uses the authorized study profile and exits 0 with 39 deferred findings. `--profile strict` retains the separate security decision; exit 2 denotes invalid/missing/stale/error evidence. Later DBs/builds can change counts. Days 5–10 now have additional execution, AI boundary and report evidence; see [current completion state](project-completion.md) and [fresh reproduction](reproduction.md). No full cluster compliance or production safety is asserted.
