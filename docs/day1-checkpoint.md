# Day 1 setup checkpoint — updated 17 October 2026

Repository: `/home/popos/Capstone/IITR-Capstone-Proj`.

**Status:** Day 1 work is complete and published on 17 October 2026. The real fork, pinned source import, supported Node/Python environments, dependency locks, production build, and finite frontend/server/API suites are verified. There were 2,334 passed tests, 8 upstream skips, and zero failures; lint passed. The user-authorized source commit `425d129` and setup/evidence/next-day-plan commit `9bca61f` were successfully pushed to `feature-16-kick-start`. See the [execution log](daily-log.md#execution-on-17-october-2026) and [evidence index](evidence-index.md).

**Documentation convention:** Every request is reflected in the relevant Markdown files before reporting completion. This file tracks current setup state; [daily-log.md](daily-log.md) records request outcomes, decisions, verification, blockers, and next steps. Personal details and credentials are omitted. The preference is also saved in personal Codex instructions outside the repository.

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
