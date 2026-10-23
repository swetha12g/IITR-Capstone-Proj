# Day 1 setup checkpoint — updated 23 October 2026

Repository: `/home/popos/Capstone/IITR-Capstone-Proj`.

**Status:** Day 1 work is complete and published on 17 October 2026. The real fork, pinned source import, supported Node/Python environments, dependency locks, production build, and finite frontend/server/API suites are verified. There were 2,334 passed tests, 8 upstream skips, and zero failures; lint passed. The user-authorized source commit `425d129` and setup/evidence/next-day-plan commit `9bca61f` were successfully pushed to `feature-16-kick-start`. See the [execution log](daily-log.md#execution-on-17-october-2026) and [evidence index](evidence-index.md).

**Latest repair and publication — 23 October:** All 11 critical issues are fixed and committed/pushed (`8ac412e`, `1616f14`). [Hosted run 39842575944](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) passed all eight jobs, confirms zero critical findings, and publishes the detailed Actions Summary/report packet. Application: 2,332 passed / six skips; 76 current contracts passed; lint/snippets and seven hosted runtime checks pass. Nine external availability tests are excluded. The local dashboard retains 180 unique issues / 91 high; hosted counts are 257 cross-stage observations, not globally deduplicated. [Verified hosted evidence](../reports/sanitized/critical-remediation/ci/verification.json). No new API call, purchase or host settings change occurred. Older dated handoffs below are historical.

**Documentation convention:** Every request is reflected in the relevant Markdown files before reporting completion. This file tracks current setup state; [daily-log.md](daily-log.md) records request outcomes, decisions, verification, blockers, and next steps. Personal details and credentials are omitted. The preference is also saved in personal Codex instructions outside the repository.

**Completion clarification — 22 October:** The ten-day implementation is delivered; full assignment acceptance remains open for independent detection labels (Day 6), successful live OpenAI evaluation (Day 8), genuine PR review (Day 9), and oral-defense/submission acceptance (Day 10). The report, reproduction, dashboard and green hosted checks are already available. Vulnerability repairs remain deferred. This status request only rechecked records and updated Markdown; no new execution, provider request, purchase, merge or submission occurred. See [remaining acceptance work](project-completion.md#remaining-assessment-work).

**Connection check — 22 October 2026:** Chat and local workspace access are working; the project records were read and updated. External services and application health were not rechecked. The project handoff below remains unchanged.

**Historical delivered baseline — 22 October before critical repair:** Days 1–10 implementation is delivered, with six scans and all eight hosted jobs passing at `bef6664` in run `39821125926`. Downloaded evidence integrity and aggregate recomputation are verified. Two fresh-directory reproductions and the final clean-PATH full run pass with temporary-cluster cleanup. The offline application profile has 2,326 passes / seven skips; nine external availability tests are excluded. All 62 current contracts and 25 source-gate contracts pass. Dashboard, deferred register, twelve-page report, defense guide and three draft remediation PRs are available; all PR workflows pass. See [current completion state](project-completion.md).

**User decisions and remaining evidence:** The acknowledgement is confirmed. Critical deferral was superseded: 11 critical issues are fixed, with zero verified locally and hosted; high/lower risks remain deferred (91 unique high in the local repair snapshot); the exact historical source approvals are unchanged. OpenAI only, existing external credential, no new purchase or further automatic call after three HTTP429 responses. Successful live AI, genuine independent labels/review and oral assessment remain open. Original cluster-health limitations are retained; no production-readiness claim is made. Tables and dated sections below retain historical setup evidence.

| Checkpoint | Status | Verified result / next action |
|---|---|---|
| Feature branch | Complete | `feature-16-kick-start`; zero commits ahead or behind origin after fetch |
| GitHub authentication | Complete | Dedicated repository SSH authentication verified; fetch succeeded |
| kubectl | Complete | v1.37.0 installed in `~/.local/bin`; official checksum and client version verified |
| Docker and kind | Complete | Docker 27.3.1 accessible; kind v0.33.0 verified |
| Bridge networking | Complete | `br_netfilter` loaded; both bridge filters enabled; Docker warnings cleared |
| Supported Node runtime | Complete | Node v24.22.0 / npm 11.19.1 installed user-locally; checksum verified; system Node unchanged |
| Python test environment | Complete | Python 3.10.12 virtual environment; pytest 9.1.1 / jsonschema 4.26.0; dependency and validation checks passed |
| Upstream provenance and source | Complete | Separate real fork; pinned commit imported; 1,466 tracked files match; MIT license preserved |
| Application build and tests | Complete with recorded skips | Root/frontend install and explicit build passed; frontend 1,372 passed; server 417 passed / 2 skipped; API 545 passed / 6 skipped |
| Scope and review role | Recorded | Individual; submission 18 October 2026; project owner is manual reviewer; independent approval/coordinator acceptance remains a separate dependency |
| Publication | Complete | Source `425d129` and setup/evidence/18 October plan `9bca61f` pushed; remote-tracking divergence verified as zero |

Bridge changes are temporary; recheck after reboot. No Kubernetes cluster has been created. Today's source and environment publication was separately authorized after the local checks and review packet were complete.

**Prior publication verified:** Closeout commit `a172539` and delivery-record commit `3bea933` were pushed to `origin/feature-16-kick-start` on 16 October. Work resumed on 17 October; the new source commit and authorized delivery are recorded in the execution log.

## 17 October completion

The six selected application stages all exited 0 and completed in 159.77 measured seconds, excluding environment setup/downloads and documentation. Dependency locks remained unchanged; all imported upstream tracked files still match after build/tests. The source has one additional local ignore override to preserve upstream-tracked public assets during a future publication, documented in [upstream-provenance.md](upstream-provenance.md).

Use `source scripts/dev-env.sh` for the project Node/Python runtimes, then `python scripts/run-day1-checks.py` to reproduce the selected checks. Full versions, checksum verification, the missing-`ensurepip` recovery, and limitations are recorded in [versions.md](versions.md).

Eight upstream tests were skipped, and Cypress E2E was not selected. No security scan jobs, live LLM triage, remediation PRs, production-safety claim, container deployment, or cluster connectivity test follows from this baseline result. Submission is 18 October; the remaining pipeline/AI/report scope is still outstanding and is not represented as complete.

## 16 October closeout (historical)

Final checks were rerun on 16 October 2026 before preparing the documentation commit:

| Check | Actual result |
|---|---|
| Git | 2.34.1; feature branch selected; fetch succeeded |
| Python | 3.10.12 |
| System Node / npm | v12.22.9 / 8.5.1; unchanged |
| kubectl | v1.37.0; resolves to `~/.local/bin/kubectl`; installed SHA-256 still matches the recorded official checksum |
| kind | v0.33.0; no clusters found |
| Docker | Server 27.3.1; zero running containers; `Warnings=null` |
| Forwarding and bridge filtering | `ip_forward=1`; both bridge-filtering sysctls equal 1; all three Docker flags true |

Today's outcome is a verified basic environment, authenticated repository access, and a reviewed compatibility plan. A supported application runtime, source provenance/import, application build/tests, and the Python test environment remain pending. The existing system Node cannot be used for the recommended Juice Shop release.

Tomorrow's ordered work items and acceptance criteria are in the [17 October JIRA-style plan](daily-log.md#plan-for-17-october-2026--jira-style-backlog). This is a Markdown planning board; no external JIRA issues have been created.

## 16 October verified local results (historical)

- Initial working tree was clean on `main`; no local work needed stashing.
- Switched safely to `feature-16-kick-start`, tracking `origin/feature-16-kick-start`, at `fbbe5bfa418a222557a71f60b6b384405c4d1abf`; origin was subsequently fetched successfully.
- Read `10-days-work-break-down.md`. SSH authentication and fetching origin succeeded after the requested account setup. Before today's documentation delivery, the feature branch matched origin at `fbbe5bfa418a222557a71f60b6b384405c4d1abf`. Earlier failures came from overly restrictive authentication options; they were not evidence that normal Git authentication was broken. No credential contents were inspected.
- Host is Linux x86_64. Existing kind reports `v0.33.0`.
- Installed kubectl `v1.37.0` for Linux amd64 into `/home/popos/.local/bin/kubectl`, mode 0755, without sudo.
- Downloaded binary and checksum from the official URLs below. SHA-256 matched before installation and remained identical after installation:

  ```text
  6129359f4e1f3848a5572ccb0b26cf28b8ca08cef38c95a765b2f64a2c961a2f
  ```

- `command -v kubectl` resolves to `/home/popos/.local/bin/kubectl`; this directory is already on PATH. No shell startup files were changed.
- `kubectl --kubeconfig=/dev/null version --client --output=yaml` reports `v1.37.0`, `linux/amd64`, and Kustomize `v5.8.1`. This deliberately avoids loading a user kubeconfig. No server compatibility smoke test has run because no cluster was created.
- Docker daemon reports `27.3.1`; `kind get clusters` reports no clusters.
- Existing system Node remains `/usr/bin/node`, `v12.22.9`; no Node installation or application import occurred.

Official binary: <https://dl.k8s.io/release/v1.37.0/bin/linux/amd64/kubectl>

Official checksum: <https://dl.k8s.io/release/v1.37.0/bin/linux/amd64/kubectl.sha256>

## Selected version pins

Use existing kind `v0.33.0` with Kubernetes `v1.37.0` and installed kubectl `v1.37.0`. The kind release explicitly lists the following node image built for that release:

```text
kindest/node:v1.37.0@sha256:a1ed56cfb0e7b93589bdf97c8cd566405a265939e3620fc4f5de89adff580ae5
```

The matching client/server minor versions satisfy Kubernetes' supported kubectl skew of plus or minus one minor version. This is documentation-verified compatibility; the image has not been pulled and a cluster has not been tested.

Recommend Juice Shop release `v20.3.0`, pinned to upstream commit:

```text
f189f521266f42c6bd05884468292000cee852ed
```

Node `v24.22.0` LTS is installed user-locally, retaining `/usr/bin/node`. The release's README marks Node 24.x supported and tested; its package metadata specifies `node: "22 - 26"`. The official Node release page identifies v24.22.0 as LTS. Node 12 is unsupported for this Juice Shop release. Root/frontend installation, the explicit production build, and selected finite tests passed with project Node 24.22.0/npm 11.19.1.

Sources checked:

- <https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0>
- <https://kubernetes.io/releases/version-skew-policy/>
- <https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/>
- <https://github.com/juice-shop/juice-shop/releases/tag/v20.3.0>
- <https://github.com/juice-shop/juice-shop/commit/f189f521266f42c6bd05884468292000cee852ed>
- <https://raw.githubusercontent.com/juice-shop/juice-shop/v20.3.0/README.md>
- <https://raw.githubusercontent.com/juice-shop/juice-shop/v20.3.0/package.json>
- <https://nodejs.org/en/blog/release/v24.22.0>

## Temporary bridge changes — APPLIED AND VERIFIED

The user authorized applying this plan. `sudo -n modprobe br_netfilter` initially stopped with `sudo: a password is required`. The user then ran the command in their own terminal. Verified that `br_netfilter` is loaded and both bridge-filtering sysctls are already 1; no sysctl writes were necessary. IPv4 forwarding remains 1. No password was requested in chat or inspected.

Docker 27.3.1 initially continued reporting the old warnings because its `RawSysInfo()` uses `sync.Once` to cache the capability checks. No containers were running when checked before a restart attempt. `sudo -n systemctl restart docker` required local authentication, so the user restarted the idle daemon in their terminal. Verification afterward confirms the Docker service is active, `IPv4Forwarding=true`, `BridgeNfIptables=true`, `BridgeNfIP6tables=true`, zero running containers, and `Warnings=null`. No kind clusters exist.

Source: <https://github.com/moby/moby/blob/v27.3.1/daemon/daemon.go#L1557-L1567>, with the reported bridge fields read from that cached object in <https://github.com/moby/moby/blob/v27.3.1/daemon/info.go#L42-L51>.

Observed before any changes:

- `bridge` and `overlay` modules loaded; `br_netfilter` not loaded.
- `br_netfilter` is available at `/lib/modules/6.9.3-76060903-generic/kernel/net/bridge/br_netfilter.ko.zst`.
- `net.ipv4.ip_forward = 1`.
- Both `net.bridge.bridge-nf-call-iptables` and `net.bridge.bridge-nf-call-ip6tables` are absent while the module is unloaded.
- Docker initially warned that both bridge filtering settings were disabled; those warnings have since cleared.
- Docker's existing bridge used `172.17.0.0/16` with gateway `172.17.0.1`; no containers were attached. Its observed DOWN/NO-CARRIER state was consistent with that idle state.
- No matching persistent settings were found in the inspected standard module-load and sysctl configuration paths.

The applied commands were run by the user in their own terminal:

```bash
sudo modprobe br_netfilter
sudo systemctl restart docker
```

Loading the module exposed both values already enabled, so no sysctl writes were needed. These read-only checks confirmed the result:

```bash
sysctl net.ipv4.ip_forward net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables
systemctl is-active docker
docker info --format 'IPv4Forwarding={{.IPv4Forwarding}} BridgeNfIptables={{.BridgeNfIptables}} BridgeNfIP6tables={{.BridgeNfIP6tables}} Warnings={{json .Warnings}}'
kind get clusters
```

Expected recorded results: all three sysctls equal 1, Docker service active, all three Docker flags true, `Warnings=null`, and no kind clusters.

Effect: bridged IPv4/IPv6 packets become visible to the corresponding IP netfilter hooks and existing firewall rules. This affects host bridges, including Docker bridges, and can alter container connectivity according to existing rules. No firewall rules, policies, routes, interfaces, forwarding settings, or persistent configuration files were edited. These warnings alone did not prove that kind would fail; runtime networking remains untested.

Both sysctls were verified as 1, and Docker's bridge warnings cleared after its restart. Container/cluster connectivity still needs a later lab test; no cluster was created for this checkpoint. These changes are temporary: no module-load or sysctl persistence files were added, so recheck after reboot.

Rollback to the observed unloaded-module state, before any cluster or other workload depends on it:

```bash
sudo modprobe -r br_netfilter
lsmod | rg '^br_netfilter\s'
sysctl net.ipv4.ip_forward
```

Successful removal restores the original absence of the bridge sysctls; `ip_forward` remains 1. An empty `rg` result is expected. If removal reports the module is in use, stop and inspect the dependency rather than forcing removal. There are no new persistence files to remove. Recheck the initial module state immediately before any future application; this rollback assumes it is still initially unloaded.

Kernel reference for the module's behavior: <https://docs.kernel.org/networking/bridge.html#netfilter>.

## Remaining checkpoints

1. Resume the [18 October Day 2 checklist](daily-log.md#plan-for-18-october-2026--jira-style-backlog) when requested; all seven planned items start unchecked.
2. Resolve the independent review/coordinator evidence arrangement where required; manual review by the project owner is recorded without fabricating GitHub approval.
3. Proceed to Day 2 source image, authored lab manifests, own kind cluster, and local runtime baseline when requested. The remaining six-stage pipeline and AI work are not implemented yet; plan against the confirmed 18 October submission date honestly.

No credentials were inspected and no cluster was created. The user applied the authorized bridge-module load and restarted the idle Docker daemon for verification; no persistent configuration files were created. Today's closeout publication is limited to reviewed Markdown documentation on the feature branch.

## Requested GitHub account setup

At the user's explicit request, this repository's local commit identity and dedicated authentication were configured for the selected GitHub account. Personal names and email addresses are omitted from this record. Global Git identity remains unchanged.

The user selected automatic generation without a passphrase. A dedicated Ed25519 key was created outside the repository with private-file permissions 0600 and public-file permissions 0644. Existing keys were preserved. No private-key contents were displayed or inspected. A repository-local `core.sshCommand` selects the dedicated key; key material and local authentication details are not included in this publication.

No global SSH configuration or other repository authentication was changed. After the user registered the public key, the SSH greeting named the intended account. Fetching origin using the dedicated key succeeded with exit status 0. The branch matched its remote-tracking branch before the closeout documentation commit.

Public-key registration is complete. Repository access can be checked without pushing:

```bash
git -C /home/popos/Capstone/IITR-Capstone-Proj fetch origin
```

The earlier successful SSH greeting exited with status 1 because GitHub does not provide shell access; the fetch exited with status 0. Neither check required inspecting credential contents.

To remove this repository's dedicated SSH selection and return to the previous default authentication, run `git config --local --unset core.sshCommand` from the repository.

## Subsequent Day 2 state — 17 October 2026

The user resumed Day 2 before the originally planned 18 October date. The historical no-cluster statements above describe Day 1 only. A source-built baseline image and owned kind lab now exist, the node/workload are Ready, and loopback HTTP plus three runtime observations are verified. Follow [day2-checkpoint.md](day2-checkpoint.md) for current deployment/CI acceptance; [daily-log.md](daily-log.md) records the request and execution. No persistent bridge settings, shell startup edits, or system Node replacement were added.

## Subsequent Day 3 state — 18 October 2026

Day 3 resumed at the user's request. Isolated pinned scanners and local source-gate/fixture tests now execute without changing system Node, shell startup or persistent bridge settings. Current scanner/gate status and remaining owner-review/hosted dependencies are in [day3-checkpoint.md](day3-checkpoint.md); request history remains in [daily-log.md](daily-log.md).

### Day 3 exact-risk decision

On 18 October the designated reviewer accepted the current 186 exact lab-only entries, expiring 25 October at 00:00 IST. Fresh local gate passes (221 visible / 186 accepted / zero blockers/errors); approved-policy hosted verification is being rerun. This changes no setup settings and is not remediation. Current handoff: [Day 3 checkpoint](day3-checkpoint.md).

### Acknowledgement assistance

The user requested assistance because the Day 4 program acknowledgement is not completed. Its LMS page link is needed to identify the actual steps; no completion/signature is recorded on the user's behalf. Day 3 verification continues, with Day 4 entry pending under the guide.

### Verified Day 3 handoff

All six PF-D3 tasks are complete; code `d68686a` / run `39111621696` passed source gates and the corrected application baseline. All 221 findings remain visible with 186 exact lab-risk approvals until 25 October at 00:00 IST; no baseline security fix is claimed. A deployment/runtime readiness race was corrected and tested. Setup/system settings are unchanged. Day 4 is unstarted pending actual program acknowledgement; the user requested help and the LMS page link is needed.

## Current setup and delivery state — 22 October 2026

The acknowledgement is confirmed and the study project has resumed through Days 5–10. This supersedes earlier pause/entry-condition notes. Project-local bootstrap has actually verified Python 3.10, pinned pip/Node and kind/kubectl without changing system packages. Current selected offline application checks pass 2,326 tests with seven skips; nine external-service availability tests are excluded. The six-stage local execution passes with deferred findings. See [current completion record](project-completion.md) for precise evidence and remaining dependencies.

No new API purchase/top-up or billing change is authorized. OpenAI only is configured; three HTTP429 generation attempts exhausted the automatic request cap. Continue local work without further paid retries. Independent human review and a successful live evaluation remain open evidence requirements.

Fresh-directory reproduction has now passed all application, scanner, runtime, mock and dashboard stages at commit `6ef16a0`; its uniquely owned temporary cluster was deleted and cleanup verified. Three separate draft PRs are published, and genuine review remains pending. No additional API purchase or call occurred during reproduction. [Receipt](../reports/sanitized/reproduction/run.json).

Continuation confirmed on 22 October. No new OpenAI generation request, purchase/top-up or billing change is made. Current delivery verification includes the explicit pinned-image prefetch correction for hosted DAST and source-free diagnostics for incomplete SAST reports. Earlier failed hosted runs remain failed; final hosted validation is still being completed.

The second fresh clone at `1e0115c` passed the full local reproduction and verified cleanup, including the different-UID permission probes. Hosted SAST diagnostics identified a per-rule/file timeout; the explicit budget is now 60 seconds with strict error handling and unchanged scope. A complete hosted pass is still being verified; no new API purchase or call has been made.

The reproduction script now preserves its project-local kind/kubectl PATH after Python activation. A clean-PATH check confirms repository-local kind, kubectl and Node selection; end-to-end verification follows. Earlier fresh-directory results used the same pinned versions and shared host caches, and are not claimed as fresh-machine runs.

### Continuation verified — 22 October 2026

The clean-PATH end-to-end run passed in 252.36 pipeline seconds without build/test reuse and removed its owned cluster. Final hosted run 39821125926 passed all eight jobs at the same code revision; all downloaded mandatory receipts share that run/revision and exact image linkage. The local dashboard now contains 371 observations / 234 underlying issues; one passive medium-instance difference from the historical 235-issue snapshot is crawl variation, not a fix. All critical/high aliases remain in the deferred register. Report/evidence and publication checks are recorded in the delivery packet; no new provider call, purchase or billing change occurred.

The refreshed delivery packet was pushed as `c7f25d9`, with zero local/remote divergence and a clean working tree at verification. It contains documentation, sanitized evidence and the inspected twelve-page PDF; tested implementation remains `bef6664`. [Publication receipt](../reports/sanitized/delivery/publication.json). No additional API call, purchase or billing change occurred.

Final repair handoff reviewed after midnight on 23 October IST: zero critical findings remain verified for the remediated local source/image and updated owned study deployment. Local tests, runtime controls, report rendering, hashes and links are checked. Ten unchanged upstream fixture lines remain in the publication scan; no new matched credential content or exception entry was introduced. Changes are uncommitted/unpushed, with no new hosted CI claim.

### Hosted critical-repair publication in progress — 23 October 2026 IST

Commit/push and hosted CI publication are now explicitly authorized. The zero-critical local snapshot above is complete; the new Actions Summary will report the actual hosted run rather than reuse its success. New hosted verification and report publication are in progress; no additional API usage or purchase is required.

Critical repairs are committed as `8ac412e`. The [Actions Summary implementation](actions-summary.md) is locally verified (76 contracts and actionlint); pushing and hosted verification are next. The earlier uncommitted local verification receipt remains an accurate historical snapshot and is not relabeled as hosted evidence.

Publication progress: `8ac412e` and `1616f14` are pushed, with zero local/remote divergence verified immediately after push. [Hosted run 39842575944](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) has passed all four source jobs and application/lint/snippet steps; the image and dependent runtime jobs remain in progress. Final acceptance requires completed aggregate/report publication and downloaded artifact verification.

### Hosted repair/report acceptance — 23 October 2026 IST

The authorized repair/report commits are pushed and [run 39842575944](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) passed all eight jobs on `1616f14`. The Actions Summary is published, and the downloaded ten-file packet passes GitHub digest verification, independent aggregate recomputation, source/run/image binding and identical-poster checks. The local repair receipt remains historical. The final documentation/evidence packet includes the downloaded receipts and identical poster; successful live AI, independent labels/review and oral acceptance remain outstanding. No provider calls, purchases, merges or reviewer messages occurred.

Final delivery verified: report/evidence packet `37b170b` is pushed, origin divergence was 0/0 and the working tree was clean at verification. Hosted tested implementation remains `1616f14`, with all eight jobs green and zero critical. The one-stop Summary, downloadable report and verification receipt are available; only the separately recorded assessment/deferred work remains.

### Goal continuation audit — 23 October 2026 IST

Hosted repair/report verification remains accepted. A fresh full-history local checkout of `b20b9b1` is running the complete reproduction with a clean PATH, project-local bootstrap and a unique owned cluster. The PDF still has stale hosted-pending wording and will be refreshed from the accepted CI receipt. Live AI/reviewer/assessment evidence remains open; no new provider call or purchase is authorized or performed.

Continuation local verification completed: fresh repaired checkout b20b9b1 passed in 274.71 pipeline seconds with all application/scanner/mock/dashboard stages and verified cleanup. Current local suite: 79 contracts plus 25 source-gate contracts. The refreshed twelve-page PDF includes accepted hosted proof and the fresh checkout; all pages rendered/inspected. Desktop/mobile dashboard displays and overflow checks pass in isolated headless Chrome. Updated report/dashboard code is ready for publication and hosted verification; no provider call, purchase or fabricated reviewer/assessment verdict occurred.

Final timing captions name the recorded fresh checkout and actual local timing run. Browser DOM checks pass at both widths; the visual proof distinguishes earlier inspected metric/layout screenshots from the final caption change whose pixel capture timed out. The PDF/input bytes remain preserved and all 79 contracts pass. Final hosted validation continues.

Current verification follow-up: 89d5db7 hosted run 39850270120 has eight successful jobs and zero critical, and its thirteen-file packet is checksum-verified. A differing server count prompted a stronger coverage gate rather than an unsupported full-suite claim: all 424 case/status identities are now required, with sequential files, dual reporters and all five critical regressions. Two local repeats pass completely; 85 contracts and actionlint pass. The fresh 89d5db7 checkout retained two bootstrap failures and is retrying with unchanged, hash-verified cached wheels. [Coverage evidence](server-test-inventory.md). Live AI and human assessment evidence remains pending.

The stronger server gate correctly failed hosted run 39908648090: Node exited zero but eleven expected verdicts were absent. Serial execution alone was insufficient. Local no-forced-exit server and API probes finish naturally with complete expected totals. Removing forced exit, retaining exact case/status equality and publishing a fresh hosted packet is in progress. The 89d5db7 fresh-checkout recovery completed in 288.61 pipeline seconds with zero critical and verified cleanup; its two setup failures remain recorded.
