# PipelineFortress daily log

This log records sanitized request outcomes and decisions. Current setup details, version pins, checksums, and rollback commands are maintained in [day1-checkpoint.md](day1-checkpoint.md). Each future request receives a concise entry here, and relevant project documents are updated before reporting completion.

## Day 1 — 2026-10-16

### Local preflight and repository discovery

- Request: locate the repository, read the execution guide, and perform read-only environment checks.
- Result: existing repository found; local work preserved. Host is Pop!_OS 22.04 LTS on x86_64 with an Intel i7-12700H, 20 CPU threads, 31 GiB RAM, and approximately 582 GiB disk available at preflight.
- Verified: Git 2.34.1, Python 3.10.12, Node 12.22.9, npm 8.5.1, Docker client/server 27.3.1, and kind v0.33.0. kubectl was initially absent.
- Limitation: hello-world image was cached; its earlier successful execution was not reverified because the initial checks were read-only. No kind cluster existed.

### Branch selection, kubectl, and compatibility checkpoint

- Request: select the feature branch, install checksum-verified kubectl without sudo, recommend compatible versions, and prepare bridge changes without applying them.
- Result: switched safely to `feature-16-kick-start`. kubectl v1.37.0 installed in `~/.local/bin`; official SHA-256 and client version verified. PATH already included that directory, so startup files were not changed.
- Decision: recorded kind v0.33.0 / Kubernetes v1.37.0 / kubectl v1.37.0 as the compatible planned combination. Recommended pinned Juice Shop v20.3.0 with a separate Node v24.22.0 installation; source and runtime remain uninstalled.
- Initial blocker: overly restrictive Git authentication options prevented fetching; later normal SSH authentication succeeded. This did not establish a fault in the existing Git configuration.

### GitHub account configuration and fetch verification

- Request: use the selected GitHub account for repository authentication and commit identity.
- Result: configured repository-local identity and a dedicated SSH key, leaving other repositories' configuration unchanged. The user selected key generation without a passphrase and registered the public key on GitHub.
- Verified: SSH greeting named the intended account; fetching origin succeeded. The feature branch matched origin with zero commits ahead or behind at verification.
- Privacy: personal names and email addresses are omitted from repository records. No private-key contents were displayed or inspected.

### Bridge-networking application and verification

- Request: apply the prepared temporary bridge plan.
- Result: local sudo authentication was required, so the user ran the privileged commands in their own terminal. Loading `br_netfilter` exposed both bridge settings already set to 1; no sysctl writes were needed.
- Verified: IPv4 forwarding remained 1. After the idle Docker daemon was restarted to refresh its cached checks, Docker reported both bridge filters enabled and no warnings. No containers were running and no kind clusters existed at verification.
- Limitation: no persistence files were created; recheck after reboot. Cluster and application connectivity have not been tested.

### Documentation and privacy updates

- Request: remove the original personal identity from repository Markdown and update the checkpoint.
- Result: removed the original name, email, and username from the checkpoint; added a current status table, verified bridge results, and remaining Day 1 tasks. Email addresses are omitted from the checkpoint.
- Verified: no matching original personal details remained in working files; Markdown fences were balanced and whitespace checks passed. No commits or pushes occurred.

### Persistent Markdown-update preference

- Request: retain the working preference in Codex and reflect every request in project Markdown.
- Result: saved the preference in the personal Codex `AGENTS.md` instruction file, outside the repository; created this daily log and linked it from the setup checkpoint.
- Convention: update the relevant document and this log after every request, including explanations, corrections, and status questions. Record verified outcomes, decisions, blockers, and next actions without full chat transcripts or sensitive details.
- Scope: this preference authorizes documentation updates; other actions still follow the user's task-specific instructions. No commits or pushes are implied.

### Today's closeout and pause

- Request: finish today's checkpoint documentation, commit and push it to `feature-16-kick-start`, prepare a JIRA-style plan for 17 October 2026, and pause until the next session.
- Result: today's basic setup checkpoint is complete. Updated [day1-checkpoint.md](day1-checkpoint.md) with the final state and explicit remaining Day 1 requirements. The guide's full Day 1 is not yet accepted because supported Node, provenance/import, build, and test work remain pending.
- Final verification: kubectl v1.37.0 and its installed SHA-256 match; kind v0.33.0 is available; Python is 3.10.12; system Node/npm remain v12.22.9/8.5.1. Docker 27.3.1 reports zero running containers, both bridge filters enabled, IPv4 forwarding enabled, and no warnings. Both bridge sysctls and IPv4 forwarding equal 1. No kind clusters exist.
- Delivery scope: commit and push only `docs/day1-checkpoint.md` and `docs/daily-log.md` to the feature branch using a normal push. Keep personal names, email addresses, credential contents, and machine authentication details out of the published records.
- Publication verified: closeout commit `a172539` (`docs: close basic setup checkpoint and plan 17 October`) was successfully pushed to `origin/feature-16-kick-start`. Privacy, Markdown-fence, staged-file scope, and whitespace checks passed. This delivery confirmation is retained in the Markdown records.
- Pause boundary: stop setup work after documentation delivery. No Node/Python packages installed, upstream source imported, or cluster created during this closeout. Tomorrow's board is a plan, not a claim that those tasks ran or authorization to run them while paused.

## Plan for 17 October 2026 — JIRA-style backlog

**Sprint goal:** finish the remaining execution-guide Day 1 requirements and obtain an evidence-backed application build/test result before moving to Day 2 deployment work.

These are local planning IDs for this Markdown board; no external JIRA tickets have been created. All items start as **To Do**. Estimated total: **5 hours**. Execute in the order below, updating actual time, status, evidence, and blockers in this log.

Execution resumed on 17 October; current task states and actual results are tracked below. The board above remains the original planned acceptance criteria.

| ID | Task | Priority | Estimate | Dependency | Acceptance criteria |
|---|---|---|---|---|---|
| PF-D1-01 | Resume and recheck the environment | High | 15 min | User resumes work | Preserve Git changes; fetch/check feature branch; verify Docker, kubectl, kind, bridge sysctls, and disk. If reboot removed the temporary module, restore it only within authorized scope. |
| PF-D1-02 | Confirm scope and upstream provenance route | High | 20 min | PF-D1-01 | Record individual/team mode, submission date, fork versus accepted import route, and reviewer/coordinator dependencies. Identify any unresolved decisions explicitly. API selection/budget may remain pending for mock-only work. |
| PF-D1-03 | Install a separate supported Node runtime | High | 30 min | PF-D1-01 | Reconfirm the chosen release's current official compatibility guidance and proposed Node v24.22.0 pin. Verify official download checksums; install user-locally without replacing `/usr/bin/node`; record Node/npm paths and versions. Explain any proposed startup-file edits before making them. |
| PF-D1-04 | Prepare Python environment and ignore rules | High | 30 min | PF-D1-01 | Add reviewed ignore rules for private reports, virtual environments, local secrets, caches, kubeconfig, and API traces. Create `.venv`; install/test pytest and jsonschema; record compatible dependency pins. Keep scanner environments separate. |
| PF-D1-05 | Acquire and record pinned Juice Shop source | High | 60 min | PF-D1-02 | Resolve the fork requirement before import. Reconfirm v20.3.0 and immutable commit `f189f521266f42c6bd05884468292000cee852ed`; record provenance and preserve LICENSE/NOTICE. Import tracked source into `app/juice-shop/` without a nested `.git` or broken submodule. |
| PF-D1-06 | Build and run documented finite tests | High | 115 min | PF-D1-03, PF-D1-05 | Inspect pinned npm scripts and engine metadata; run `npm ci`, the documented build, and non-watching CI/unit tests. Preserve the lockfile. Record commands, exit codes, selected suites, duration, and sanitized evidence; report failures honestly. |
| PF-D1-07 | Complete Day 1 records and review the next checkpoint | High | 30 min | PF-D1-04, PF-D1-06 | Update versions, provenance, scope/requirements, daily log, and evidence index. Mark Day 1 passed only when branch, provenance/license, Docker, build, tests, and staged-content checks pass. Review a scoped documentation/source diff and agree on the next publication step. |

### 17 October working checklist — completed

- [x] Resume explicitly and read the current checkpoint and this board.
- [x] PF-D1-01 — environment recheck passed.
- [x] PF-D1-02 — scope and provenance route recorded; unresolved dependencies named.
- [x] PF-D1-03 — supported Node installed separately; system Node preserved.
- [x] PF-D1-04 — Python test environment and ignore rules verified.
- [x] PF-D1-05 — pinned upstream source and license provenance recorded.
- [x] PF-D1-06 — application build and selected finite tests passed, or blockers documented.
- [x] PF-D1-07 — local Day 1 acceptance, evidence records, and publication candidates reviewed; commit/push scope explicitly authorized.

### Dependencies and limits

- The temporary bridge configuration must be rechecked after reboot; warning-free Docker output alone is not a cluster networking test.
- System Node 12 is unsuitable for the recommended Juice Shop release; app installation/build waits for the supported runtime.
- If fork/provenance acceptance is unresolved, continue independent environment/documentation tasks and mark source acquisition blocked rather than silently importing.
- No live LLM API calls, keys, cluster creation, scanning of external targets, or automatic pushes are part of this next-day plan. Revisit those steps when their prerequisites and scope are agreed.
- If the five-hour estimate is exceeded, record the actual result and revised plan; do not mark unfinished Day 1 work complete to advance the calendar.

## Execution on 17 October 2026

The user resumed work and requested completion of today's board. After the local acceptance checks and concrete review packet were ready, the user explicitly authorized committing and pushing the reviewed Day 1 work to `feature-16-kick-start`.

| Ticket | Current status | Actual result |
|---|---|---|
| PF-D1-01 | Done | Clean feature branch, successful fetch, approximately 582 GiB free disk, warning-free Docker, both bridge sysctls enabled, verified kind/kubectl; no clusters |
| PF-D1-02 | Done with external review dependency noted | Individual scope confirmed; real fork verified; submission 18 October 2026 and project-owner manual review confirmed. Independent approving review/coordinator assessment interpretation remains separate and unconfirmed |
| PF-D1-03 | Done | Official Node v24.22.0 archive checksum passed; user-local Node/npm 24.22.0/11.19.1 selected via `scripts/dev-env.sh`; system Node 12.22.9 unchanged; no startup-file edits |
| PF-D1-04 | Done | Added ignore rules; recovered missing `ensurepip` through temporary `virtualenv`; Python 3.10 environment, pytest 9.1.1, jsonschema 4.26.0, dependency and valid/invalid schema checks passed; exact requirements recorded |
| PF-D1-05 | Done | Fork commit fetched; archived source into `app/juice-shop/`; all 1,466 tracked files match, MIT license preserved, no nested `.git` |
| PF-D1-06 | Done | Root/frontend installation and explicit production build passed; frontend 1,372 passed, server 417 passed / 2 skipped, API 545 passed / 6 skipped; zero failures; dependency locks unchanged |
| PF-D1-07 | Done and published | Records and source/import/privacy checks complete; lint passed; commits `425d129` / `9bca61f` pushed to the feature branch with zero divergence verified |

### Implementation decisions and recovery

- `python3 -m venv` could not seed pip because host `ensurepip` is absent. A temporary PyPI `virtualenv` tool created `.venv` without system-package installation; Python dependencies were installed and verified inside it.
- The upstream application does not track npm lockfiles. Resolved exact root/frontend locks with scripts disabled, recorded them under `locks/juice-shop/`, and kept the imported tracked tree unchanged. The runner checks lock stability after execution.
- The runner captures raw output only under ignored private evidence and writes sanitized run manifests with commands, exit codes, duration, and log checksums. Cypress E2E and live LLM API calls are excluded from this Day 1 check selection.
- Public upstream license/attribution remains intact. Newly written project Markdown omits user names, email addresses, and credentials.

Per-ticket actual time was not independently timed; the planned estimates above are not presented as measured effort. Application stage durations are recorded in the runner's UTC-timestamped manifests.

### Verified completion and review packet

- All selected installation/build/test stages passed in 159.77 measured seconds, excluding setup/downloads and documentation. The run ID is `20261016T183808Z` in UTC, corresponding to 17 October 2026, 00:08:08–00:10:48 IST.
- Totals: 2,342 tests counted, 2,334 passed, 8 skipped, 0 failed. Eight upstream skips and the exclusion of Cypress E2E remain explicit limitations.
- The recorded dependency locks did not change. Rechecked all 1,466 imported upstream tracked files after execution; none changed. Production server/frontend outputs exist and remain ignored.
- Content review caught ten public upstream files that ordinary Git staging would omit because of ignore patterns. Added narrow publication exceptions for the nine existing JavaScript assets and one public challenge fixture; the complete pinned source is now visible without broadly forcing ignored files into the index.
- Private logs, Python environment, node_modules, API traces, and local alias maps are excluded from publication candidates. Lockfile resolved URLs contain no embedded authentication. New project Markdown passed personal-detail and fence checks, and whitespace checks passed. No full secrets-scanner verdict is claimed for the deliberately vulnerable public upstream fixtures.
- Review references: [checkpoint](day1-checkpoint.md), [versions](versions.md), [scope](scope.md), [provenance](upstream-provenance.md), [requirements](requirements-checklist.md), [evidence index](evidence-index.md), and [report outline](final-report.md).
- The user subsequently authorized publishing the reviewed source, environment helpers, locks, Markdown, and sanitized evidence. The pinned source is isolated in commit `425d129`; publication results will be verified before reporting delivery complete.

### Submission-date and reviewer update

- Request: record submission on 18 October and the user as reviewer.
- Result: recorded **18 October 2026** and **project owner as manual reviewer** without personal contact details. The exact submission cutoff time was not supplied.
- GitHub does not permit authors to approve their own PRs. Manual review notes will be retained honestly, with coordinator acceptance/independent approval requirements distinguished from self-review; no approval has been invented.
- The submission date is one calendar day after this execution date. Source containerization, local deployment, security scans/gates, metrics, AI safeguards/evaluation, three reviewed remediation PRs, and the final report remain outstanding. No full-project deadline-readiness claim is made.

### Authorized publication and upstream review

- Request: commit and push the reviewed Day 1 work to `feature-16-kick-start`.
- Precommit verification: the upstream-required `npm run lint` passed with exit 0 in 8.57 seconds. The source-only index was checked against the 1,466 pinned upstream files plus the one narrow local ignore override; generated/private files were absent.
- Source commit: `425d129` (`chore: import pinned Juice Shop v20.3.0 baseline`), with required DCO sign-off in Git metadata. Personal commit details are not copied into Markdown.
- Whitespace review: the unchanged upstream snapshot has 190 pre-existing whitespace diagnostics. Preserved the verified pinned bytes rather than reformatting upstream source; the new local override passed its whitespace check. This is distinct from the successful lint/build/test results and is retained in sanitized review evidence.
- Environment, locks, documentation, sanitized evidence, completed 17 October ticks, and the 18 October board were committed separately as `9bca61f`. A normal push of both commits to `origin/feature-16-kick-start` succeeded; working tree was clean and ahead/behind counts were `0 / 0` at delivery verification. No private evidence, Python environment, or node_modules files were tracked.

### Requested final cross-check and next-day planning

- Request: cross-check 17 October again, tick the completed JIRA checklist, and prepare the same style of checklist for 18 October from `10-days-work-break-down.md`.
- Cross-check: the committed source blob IDs and file modes match all 1,466 upstream tracked files; build outputs exist; private test-log checksums match the sanitized manifest; all selected stages passed; lint passed; eight upstream test skips remain recorded. Project Node, Python dependency consistency, Docker warnings, and bridge settings were rechecked.
- Result: PF-D1-01 through PF-D1-07 are checked and their source/environment/evidence records are published. Remote delivery succeeded and was verified; 18 October tasks remain unchecked.
- Planning: 18 October follows the guide's **Day 2**, with image, own kind lab, runtime baseline, and baseline CI tasks. Because 18 October is also the stated submission date, the board includes an explicit submission gap review; unfinished Days 3–10 are not relabeled as completed.

## Plan for 18 October 2026 — JIRA-style backlog

**Sprint goal:** complete the guide's Day 2 baseline: source-built image, running owned kind lab, local HTTP evidence, three confirmed runtime observations, and a successful baseline build/test/deployment workflow.

**Date and deadline:** 18 October 2026, Asia/Kolkata. The exact submission cutoff time is unconfirmed. After Day 1, the guide still allocates **45 focused hours to Days 2–10**; this **five-hour Day 2 plan does not complete that remaining scope**. The final report/AI/security requirements remain blocking gaps for a complete submission, and no complete submission is promised by this board.

These are local Markdown planning IDs, not external JIRA issues. The user requested execution on **17 October**, bringing this board forward from 18 October. Planned total: **300 minutes / 5 hours**. See the Day 2 execution entry below for verified results; pending items remain unchecked.

| ID | Task | Status | Priority | Estimate | Dependency | Acceptance criteria |
|---|---|---|---|---|---|---|
| PF-D2-01 | Resume, recheck Day 1 evidence, and review submission gaps | Done with cutoff/review questions open | Highest | 20 min | Day 1 delivery | Preserve changes, fetch/check branch, select project runtimes, recheck Docker/bridge filters after reboot, review recorded test skips, confirm cutoff time and actual deliverable gaps. Record unresolved coordinator/review decisions honestly. |
| PF-D2-02 | Build the baseline image from pinned source | Done | High | 50 min | PF-D2-01 | Inspect the upstream Dockerfile/build context and recorded locks; build `pipelinefortress:baseline` from `app/juice-shop/`. Verify image ID, source commit, architecture, and expected port; capture sanitized evidence. A downloaded prebuilt app image is not sufficient. |
| PF-D2-03 | Author and validate owned lab manifests | Done | High | 30 min | PF-D2-01 | Create `infra/kind.yaml` for one control-plane and namespace/deployment/ClusterIP service manifests under `infra/k8s/`. Use matching labels, verified port 3000, readiness probe, resource settings, the baseline tag and `IfNotPresent`. Validate YAML/schema; no public ingress or LoadBalancer. |
| PF-D2-04 | Create the local kind lab and verify readiness | Done | High | 60 min | PF-D2-02, PF-D2-03 | Use the recorded compatible node-image digest, create the named `pipelinefortress` cluster, load the exact source-built image, apply manifests, and verify node Ready, successful rollout, and ready pods. Inspect any failures privately and record actual results. |
| PF-D2-05 | Verify loopback HTTP and document the runtime baseline | Done | High | 50 min | PF-D2-04 | Forward the service on `127.0.0.1:3000` only, verify HTTP, capture a sanitized screenshot/workload status, and write at least three locally confirmed insecure behaviors with safe reproductions, expected behavior, risk, and evidence. Keep suspicions separate from confirmed observations. |
| PF-D2-06 | Implement and run baseline GitHub Actions | In progress: hosted run | High | 60 min | PF-D2-02, PF-D2-03 | Create root `.github/workflows/security.yml` for feature pushes/PRs with `contents: read`, verified action SHAs, timeouts, and a pinned supported runner. Use recorded app/runtime/lock paths, finite build/tests, and a separate ephemeral runner kind cluster with cleanup. Run the agreed workflow and record its actual URL/result; never target laptop localhost from hosted CI. |
| PF-D2-07 | Review evidence and prepare an honest submission status | To Do | Highest | 30 min | PF-D2-05, PF-D2-06 | Update versions, runtime report, evidence index, requirements, report outline, and this log. Project owner performs real manual review. Review the safe diff/publication scope and record all remaining mandatory gaps before any submission/tag. Do not label a Day 2-only result as a complete capstone or invent approval/run evidence. |

### 18 October working checklist

- [x] PF-D2-01 — environment and submission gap review recorded.
- [x] PF-D2-02 — exact baseline image built from pinned source and inspected.
- [x] PF-D2-03 — lab manifests authored and validated.
- [x] PF-D2-04 — owned kind node and app rollout Ready.
- [x] PF-D2-05 — loopback HTTP, sanitized screenshot, and three confirmed runtime observations recorded.
- [ ] PF-D2-06 — baseline CI build/tests and runner deployment succeeded; run URL recorded.
- [ ] PF-D2-07 — evidence, manual review notes, truthful submission status, and safe publication scope reviewed.

### Day 2 acceptance from the execution guide

- [x] Source-built image exists with recorded identity.
- [x] Local kind is Ready.
- [x] Application HTTP is reachable locally.
- [x] Confirmed runtime baseline report exists.
- [ ] CI build/test run succeeds.
- [ ] Actual CI run URL is recorded.

### Remaining mandatory submission gaps — not completed by this Day 2 plan

- [ ] Day 3: Semgrep, dependency and secrets scans with bad/fixed gates and failure handling.
- [ ] Day 4: Checkov custom policies, functional image/IaC hardening, exact-image scan, and Syft SBOM; required acknowledgement before this stage.
- [ ] Day 5: ZAP baseline and all six mandatory jobs with a fail-closed aggregate gate.
- [ ] Day 6: normalization, independent ground-truth labels including misses, and a recomputable metrics dashboard.
- [ ] Day 7: tested source-free redaction, captured mock-body checks, injection/refusal cases, and zero-call refusals.
- [ ] Day 8: explicitly budgeted real API triage after safeguards, grounding validation, honest FP/FN results, and cost/model disclosure.
- [ ] Day 9: three genuine AI-assisted remediation PRs with before/after tests and genuine review evidence; resolve independent approval/coordinator acceptance as applicable.
- [ ] Day 10: fresh reproduction, evidence-backed 12-page rendered report, maturity assessment, disclosure, final audit, and oral-defense preparation.

If deadline/capacity cannot accommodate the mandatory evidence, record the actual partial result and discuss acceptable assessment scope with the coordinator. Do not skip redaction, human review, or mandatory tools to create an unsupported completion claim. No external messages or deadline-extension requests are sent by this plan.

## Day 2 execution started 17 October 2026

- Request: start and complete the guide's Day 2 in the established workflow, ahead of the original 18 October board date.
- Recheck: fetch succeeded on the correct branch; Day 1 evidence and recorded eight skips remain valid. Docker/bridge filters and project runtimes passed current checks. Submission cutoff and independent-review interpretation remain open external facts.
- Actions: source image build exited 0; pinned kind/Kubernetes 1.37.0 lab created with a dedicated ignored kubeconfig; namespace/deployment/ClusterIP service passed server dry-run and rolled out Ready. The running image identity was matched through CRI.
- Runtime: HTTP 200 home page, unauthenticated directory listing and metrics, plus malformed-search SQL/stack error disclosure confirmed using reads against the owned loopback target. Raw bodies/logs remain private; see [runtime baseline](runtime-baseline.md).
- Screenshot: browser-control inventory had no browser and opening the in-app browser failed. User explicitly authorized isolated headless Playwright for the local screenshot; capture and image review passed. Non-loopback requests were blocked and no personal data was entered.
- CI: authored SHA-pinned workflow, passed actionlint and shell/Python syntax checks; implementation commit `f9867e0` was reviewed and pushed normally; [hosted run 38954124002](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38954124002) is in progress.
- Next: record the actual hosted result, complete the evidence/checklist cross-check and publication, and preserve the remaining submission gaps.

### Day 2 reviewer response — 17 October 2026

- Request/outcome: the designated reviewer explicitly confirmed reviewing and accepting the local Day 2 evidence, including the runtime report and running-app screenshot.
- Limitation: hosted CI was still pending at that confirmation; independent approving PR review is not claimed.
- Next: finish the actual hosted run, cross-check all acceptance evidence, publish the final records and stop at the Day 2 boundary.

### Day 2 reproduction correction

- Review finding: replacing `pipelinefortress:baseline` in kind leaves an existing pod unchanged unless the deployment template changes.
- Action: added an image-config-ID pod-template annotation in `scripts/deploy.sh`; changed image identity triggers a rollout. Syntax/actionlint checks passed; local rerun and hosted verification are required for the corrected helper.
- The initial hosted run passed application build/tests and tool checksum verification. A new code push will supersede it under the workflow's concurrency policy; no cancelled/superseded result will be counted as final acceptance.
