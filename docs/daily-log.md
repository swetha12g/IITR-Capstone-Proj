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
| PF-D2-06 | Implement and run baseline GitHub Actions | Done; prior incident cause unconfirmed | High | 60 min | PF-D2-02, PF-D2-03 | Create root `.github/workflows/security.yml` for feature pushes/PRs with `contents: read`, verified action SHAs, timeouts, and a pinned supported runner. Use recorded app/runtime/lock paths, finite build/tests, and a separate ephemeral runner kind cluster with cleanup. Run the agreed workflow and record its actual URL/result; never target laptop localhost from hosted CI. |
| PF-D2-07 | Review evidence and prepare an honest submission status | Done | Highest | 30 min | PF-D2-05, PF-D2-06 | Update versions, runtime report, evidence index, requirements, report outline, and this log. Project owner performs real manual review. Review the safe diff/publication scope and record all remaining mandatory gaps before any submission/tag. Do not label a Day 2-only result as a complete capstone or invent approval/run evidence. |

### 18 October working checklist

- [x] PF-D2-01 — environment and submission gap review recorded.
- [x] PF-D2-02 — exact baseline image built from pinned source and inspected.
- [x] PF-D2-03 — lab manifests authored and validated.
- [x] PF-D2-04 — owned kind node and app rollout Ready.
- [x] PF-D2-05 — loopback HTTP, sanitized screenshot, and three confirmed runtime observations recorded.
- [x] PF-D2-06 — baseline CI build/tests and runner deployment succeeded; run URL recorded.
- [x] PF-D2-07 — evidence, manual review notes, truthful submission status, and safe publication scope reviewed.

### Day 2 acceptance from the execution guide

- [x] Source-built image exists with recorded identity.
- [x] Local kind is Ready.
- [x] Application HTTP is reachable locally.
- [x] Confirmed runtime baseline report exists.
- [x] CI build/test run succeeds.
- [x] Actual CI run URL is recorded.

### Remaining mandatory submission gaps — not completed by this Day 2 plan

- [x] Day 3: Semgrep, dependency and secrets scans, bad/fixed probes, fail-closed contracts and exact owner review (approved-policy source and corrected baseline CI passed).
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

- Rerun outcome: changed template rolled out; unchanged-image second apply reported no patch change; runtime recheck passed on the replacement pod. Corrected implementation `c1d78b9` was pushed normally. Final verification is [run 38955433523](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38955433523); awaiting its actual result.

## Next checkpoint backlog — Day 3, planned for 18 October 2026

Day 2 was brought forward to 17 October. Execution started on **18 October 2026** at the user's request. This is the JIRA-style Markdown board, based on the guide's Day 3; no external JIRA issues or scanner installations are created by this plan. Target timebox: 300 minutes. The remaining Days 3–10 still total approximately 40 focused hours, so this board is not a promise of a complete submission on 18 October. Exact cutoff/coordinator interpretation remains unresolved.

| ID | Task | Status | Priority | Estimate | Acceptance criteria |
|---|---|---|---|---|---|
| PF-D3-01 | Verify and pin official Semgrep, Trivy and Gitleaks tools; configure reviewed rules | Done: local and hosted verification | High | 120 min | Official versions/checksums and supported CLI flags recorded; meaningful JS/TS rules and narrow generated/vendor exclusions; application source remains in scope |
| PF-D3-02 | Run source, dependency, full-history and working-tree scans | Done: local and hosted verification | High | 45 min | Private machine-readable output; timestamps/exit codes captured; full Git history fetched in CI; distinguish findings from scanner execution errors |
| PF-D3-03 | Triage baseline and define exact expiring exceptions | Done: 186 exact lab-only entries approved | High | 15 min | Rule/advisory, component/path fingerprint, reason, owner role, expiry and baseline commit; no blanket application suppression |
| PF-D3-04 | Implement scan wrapper and fail-closed gate policy | Done: local and hosted verification | Highest | 60 min | Explicit severity mappings; invalid/missing JSON, crashes, mandatory skips and expired exceptions block; collect all reports without blanket passing error suppression |
| PF-D3-05 | Prove bad/fixed behavior with isolated synthetic fixtures | Done: local and hosted verification | High | 30 min | Unsafe source pattern, verified advisory fixture and token-shaped canary detected; repaired/removed fixtures pass relevant gates; no real credential or seeded deployed feature |
| PF-D3-06 | Run hosted checks and review sanitized evidence | Done: source gate and corrected baseline CI passed | High | 30 min | Actual run URL/results, policy tests, JSON validation and baseline risk visible; no raw secret matches in public output; update requirements/report/evidence |

- [x] PF-D3-01 — official tool pins and reviewed scanner configuration.
- [x] PF-D3-02 — three scanners execute with valid private reports, full history and working-tree coverage.
- [x] PF-D3-03 — 186 exact reviewed lab exceptions; expiry 25 October 00:00 IST.
- [x] PF-D3-04 — fail-closed operational-error and expiry tests.
- [x] PF-D3-05 — real scanner detection of synthetic bad/fixed fixtures.
- [x] PF-D3-06 — actual hosted evidence and safe Markdown closeout.

Entry dependency: accepted Day 2 baseline. The user resumed Day 3 on 18 October; task states below will follow actual verification. Day 4 acknowledgement and later live-AI configuration/budget remain separate requirements.

### Hosted verification progress

Corrected run `38955433523` passed application build/tests and official kind/kubectl checksum installation. The source-image build and subsequent runner deployment/runtime are still running; PF-D2-06 and final closeout remain unchecked until the complete job succeeds. The superseded first run concluded cancelled and is not counted as acceptance.

### User-linked failed hosted job — 17 October 2026

- Request: inspect [job 117157402202](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38955433523/job/117157402202) while completing Day 2.
- Verified result: application build/tests, verified tools and image build succeeded; deployment exited 1 after about 247 seconds, runtime was skipped, artifact upload and cluster cleanup succeeded. No full Day 2/CI success is claimed.
- Evidence limitation: the visible job log contains only the deployment exit code; private runner output was not uploaded. Its sanitized artifact contains only the passing test manifest. Root cause remains unknown.
- Action: added an early kind-startup diagnostic phase, retained failed owned nodes until cleanup, selected disk/node/pod/kubelet probes and redacted failure JSON. Synthetic privacy checks, actionlint and syntax checks passed. This is instrumentation, not an assumed root-cause fix or relaxed gate.
- Investigation method: applied the local investigate skill. Its startup/freeze/learnings helpers are absent at their configured paths, so degraded local investigation is used without installing/upgrading the skill or changing settings. Helper restoration via `/gstack-upgrade` is separate from this task.
- Next: publish the diagnostic change, capture the actual failure cause, apply a verified minimal fix and rerun full acceptance.

### Diagnostic-run narrowing

Run `38957969793` for instrumentation commit `280514f` passed early kind startup on the hosted runner, then proceeded to application build/tests. The earlier failure therefore cannot be labeled a general unsupported kind/Kubernetes combination. Post-build deployment diagnostics are pending; build-related resource changes are a hypothesis, not an established cause. The downloaded first failure artifact SHA-256 matched GitHub metadata; its six application stages all exited 0 with unchanged locks, retained separately as `reports/sanitized/day2/ci-failed-run-build-tests.json`.

## Day 2 closeout — 17 October 2026

- Outcome: **all seven PF-D2 tasks and all six guide acceptance checks passed**. [Run 38957969793](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38957969793) completed successfully for `280514f`, including six application stages, verified tools, early kind startup, source image, own runner cluster, four runtime checks, artifact upload and cleanup.
- Evidence: downloaded artifact `12071418832` matched its official SHA-256; validated build/test and runtime records are retained under `reports/sanitized/day2/ci/`, with a [CI receipt](../reports/sanitized/day2/ci-receipt.json). Local source/locks remained unchanged and private kubeconfig/logs remain untracked.
- Review: actual local manual review was confirmed by the designated reviewer; engineering checks and actual hosted evidence passed. No independent PR approval or human review of the later hosted result is fabricated.
- Incident limitation: first run was superseded/cancelled; second run failed during deployment with its private log lost. Exact historical cause remains unconfirmed. The new run passed with early startup validation and redacted future failure diagnostics; this is not presented as a proven historical root-cause fix.
- Records: updated Day 1 handoff, Day 2 checkpoint, runtime/screenshot report, versions, requirements, evidence index, report outline, README and the JIRA ticks. The Day 3 board remains wholly unchecked.
- Delivery verified: reviewed Markdown/sanitized evidence closeout `204ae02` was normally pushed to `origin/feature-16-kick-start`. Working tree was clean and ahead/behind counts were `0 / 0` at verification; private kubeconfig/artifact ZIPs remained ignored. This receipt follows that completed delivery. Stop at Day 2. The local cluster remains Ready; temporary port-forwards are closed. Days 3–10 and the full submission are not complete.

## Day 3 execution — 18 October 2026

- Request: continue the Day 3 activities planned in this log and `10-days-work-break-down.md`, keeping both records synchronized.
- Recheck: clean feature branch preserved; fetch succeeded and branch matched origin. Full Git history and project runtimes verified; sufficient disk available.
- Actions: checked official scanner releases and CLI documentation; preparing isolated checksum-verified tools and reviewed source rules.
- Boundary: scan repository/application inputs only; keep raw findings private, avoid credential files, preserve imported source, and distinguish findings from scanner failures. Day 4 and live AI are not started.
- Next: run all three scanners, triage exact fingerprints, implement/test fail-closed gates and synthetic bad/fixed probes, then verify hosted evidence and update acceptance honestly.

### Day 3 local scanner/gate verification

- Official tool checksums and a 66-distribution Semgrep hash lock passed; all scanners run in ignored project-local tools. No system installation or imported app changes.
- Actual reports: Semgrep 11 matches / 643 files / zero parser errors after 12 exact teaching-fragment exclusions; Trivy 70 raw/distinct dependency findings; Gitleaks 69 raw rows per history/tree scan, 68 distinct locations each. Source-import provenance matched all 24 secret-match files without publishing match values.
- Gate: 217 distinct findings, 183 blocking before review, zero scanner/report operational errors. Prepared [review packet](day3-baseline-review.md) and exact expiring proposals. Owner decision is pending; active exceptions remain empty.
- Verification: 24 fail-closed/metadata-privacy contract tests passed; real scanner bad/fixed fixtures passed their expected outcomes; a separate history probe stayed blocked after tree removal. No raw secret, real credential validation or deployed fixture was used.
- Next: verify the hosted workflow and record its actual result; retain a blocking production gate until the designated reviewer accepts exact baseline risk or issues are remediated. Day 4 remains unstarted.

### Day 3 hosted source result

- Published implementation `1dad4b7`; [run 39107551251](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39107551251) is running the baseline job. Source job `117616578672` completed tool verification, 24 tests, actual scanner fixtures and all scan collection successfully.
- Its gate correctly failed on 183 unapproved baseline risks, with zero operational errors; this is not a successful production gate. Owner approval is still pending and the active exception list remains empty.
- Downloaded source artifact `12128659514`; official ZIP checksum matched. All 217 fingerprints and file bindings matched local reports; no generated canary, raw match values/lines or contact fields appeared in sanitized records.
- Next: finish the parallel baseline run, retain actual hosted results and await the designated owner's exact baseline review. No Day 4 work is started.

### Day 3 development-dependency coverage correction

- Found that the first Trivy command followed its production-only default. Corrected collection to include development dependencies and made that scope mandatory in the gate manifest; added a regression contract.
- Corrected local result: Semgrep 11, Trivy 74 raw/distinct findings, Gitleaks 69 raw rows per history/tree scan with 68 distinct locations each; 221 distinct findings total, 186 blockers, zero operational errors. All 25 contract tests and real scanner fixtures pass their expected outcomes.
- The previous 183-entry packet is archived and superseded by [186 exact proposals](../reports/sanitized/day3/baseline-review-proposals.json). Three additional high findings require acceptance of the updated packet; no earlier approval can silently widen to them. Owner review is still pending and active exceptions remain empty.
- First hosted source evidence remains valid for its recorded production-only scope, not final corrected-scope acceptance. Next: publish/reverify the coverage correction and await the designated owner's decision on the current packet.

The first run's parallel baseline job `117616578703` completed successfully, including deployment/runtime and cleanup. Source-gate rejection was its only failed stage. The expanded dependency scope still requires a new hosted source verification; owner review remains pending.

### Corrected hosted source evidence — owner decision pending

Run `39108322664` / source job `117618870374` verified the corrected production/development scope: tools, 25 contracts, real fixtures and collection succeeded. The gate rejected exactly 186 unapproved risks with zero operational errors. Downloaded artifact `12129287626` matched its official SHA-256; all 221 identities/content bindings matched local evidence, and artifact/log privacy checks passed. The parallel baseline job is still running. Owner approval of the current packet has not been received; no exception is enabled and Day 3 is not claimed complete.

## Day 3 technical closeout — 18 October 2026

- Five planned PF-D3 tasks are verified locally and in hosted CI. PF-D3-03 remains open: the designated owner has not approved the current 186 exact baseline-risk proposals. No response or elapsed time is approval; active exceptions remain empty. The earlier 183-entry request is superseded.
- Corrected [run 39108322664](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39108322664) for `421f8eb` concluded **failure solely at the expected source policy gate**: 221 findings, 186 unapproved blockers, zero operational errors. Tools, 25 contracts, live bad/fixed/history probes and collection passed. Production and development dependencies were both included.
- Parallel baseline job `117618870178` passed all application install/build/test stages, source image, owned kind deployment, runtime and cleanup. Source job `117618870374` uploaded sanitized evidence after its risk rejection. Both artifact ZIP hashes matched official metadata; source identities/content hashes matched local data, and source artifact/log privacy checks passed.
- Updated guide checkboxes, Day 3/review documents, Day 1 handoff, versions, requirements, evidence index, README and report outline. Implementation was normally pushed; final documentation/evidence delivery is being verified. Imported source/app locks and private-data exclusions were preserved.
- Remaining action: project-owner reviewer decides on [the current 186-entry packet](day3-baseline-review.md). Approval would enable only those exact content/severity/commit-bound lab exceptions until 25 October at 00:00 IST; new/changed risks and operational errors still block. Rejection keeps the gate blocked. Day 3 is not declared complete and Day 4 has not started.

### Final count-label and publication verification

Corrected a prose counting error: the two de-duplications belong to the secret scans (69 raw rows / 68 locations each), not dependencies (74 raw / 74 distinct in the expanded scope). Total 221 and blocking 186 are unchanged, as are every proposal fingerprint and content binding. The publication audit confirms the same 68 tree-location fingerprints and zero new locations. The checksum-index check was scoped to the Day 3 section to avoid colliding with a same-named Day 2 receipt; all current hashes matched. Closeout `7c876e0` was normally pushed and verified clean at `0 / 0`; this correction preserves the pending owner-review item.

## Exact baseline review received — 18 October 2026

- Request: keep the project for study/experimentation, fix findings and proceed; the designated reviewer explicitly accepted the **current 186 exact lab-only exceptions** in the updated packet.
- Action: activated only those reviewed fingerprints/severities/content bindings, expiring **25 October 2026 at 00:00 IST**. The older 183-entry proposal remains superseded. New/changed findings and scanner failures still block. No personal contact details are recorded.
- Verification: fresh local scans, policy contracts and hosted confirmation are being rerun; no new successful gate is claimed yet. Acceptance is a time-limited risk decision, **not remediation**. Actual hardening/fixes will have separate before/after evidence in the guide's next stages.
- Next: close Day 3 after actual verification. Day 4 requires the guide's Responsible AI Use and Lab Conduct acknowledgement; completion/date has been requested, with any signed record kept private.

### Approved-policy hosted source gate — 18 October 2026

Commit `c88ec1f` / [run 39110505372](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39110505372), source job `117625451381`, passed tools, all 25 contracts, real scanner probes, full collection and the approved source gate. The downloaded artifact ZIP matched its official hash; all 221 identities/content bindings match local data, with 186 accepted risks, zero blockers and zero operational errors. Metadata/privacy checks passed. Parallel application baseline is still running; its final result is not assumed. Day 4 acknowledgement remains unconfirmed, so hardening has not begun.

## Day 4 hardening checklist — current state on 22 October

These are Markdown planning IDs, not external JIRA issues. The user confirmed the acknowledgement on 22 October and implementation resumed. Earlier dated entries below retain their historical state. No risk is marked fixed by accepting an exception; signed material remains private.

| ID | Planned task | Status | Evidence needed |
|---|---|---|---|
| PF-D4-00 | Confirm Responsible AI Use and Lab Conduct acknowledgement completion/date | Complete | User confirmation received 22 October; signing date unspecified; no signed record stored |
| PF-D4-01 | Pin and run Checkov with a custom immutable-image policy | Verified locally | Checkov 3.3.30, 100 hashed distributions, eight CLI fixtures, CKV_PF_K8S_1 actually runs |
| PF-D4-02 | Map applicable controls and document gaps | Verified bounded mapping | CIS 2.0.0 workload mapping with explicit gaps; no cluster certification |
| PF-D4-03 | Build a functional hardened image | Verified locally | Pinned bases, production dependencies, clean context; seven Docker HTTP checks and enforcement tests |
| PF-D4-04 | Apply/test Kubernetes hardening in the owned local lab | Verified locally | Ready rollout, zero restarts, exact image match, seven HTTP checks and process/filesystem tests |
| PF-D4-05 | Scan and inventory the exact hardened image | Verified locally | Frozen-DB comparison and 2,748-component schema/package-validated CycloneDX 1.6 SBOM |
| PF-D4-06 | Compare baseline and hardening results, update gate/evidence | Evidence verified; acceptance open | 15 gate contracts pass; real gate blocks on one IaC and 38 high/critical image findings; no new risk approvals |

- [x] PF-D4-00 — acknowledgement entry condition confirmed by user.
- [x] PF-D4-01 — Checkov built-in/custom fixtures.
- [x] PF-D4-02 — mapped controls/gaps.
- [x] PF-D4-03 — functional hardened image.
- [x] PF-D4-04 — tested Kubernetes hardening.
- [x] PF-D4-05 — same-image scan/SBOM.
- [ ] PF-D4-06 — comparison/gate implemented; residual security acceptance remains open.

Three focused AI-assisted remediation PRs remain a separate Day 9 requirement; source-free AI safeguards, provider/model/budget and genuine review evidence must precede that claim. No live model call, new local cluster or application source patch was made during this approval closeout. Hosted CI uses its own ephemeral cluster.

### Acknowledgement assistance requested — 18 October 2026

- Request: the user reported being unable to complete the program acknowledgement and asked the assistant to handle it.
- Outcome: technical work can be delegated, but no personal attestation/signature or completion date is fabricated. The guide's Day 4 entry condition remains **not completed**. Requested the program/LMS page link to help locate the actual steps; no credential or signed document was requested.
- Action: continue closing verified Day 3 work and its hosted run. Day 4 implementation remains unstarted until the actual acknowledgement requirement is satisfied.

### Hosted deployment wait race and local correction

- Run `39110505372` source job passed the approved Day 3 gate. Its baseline build/tests and image build passed, but deployment returned exit 1 at the **post-rollout label-wide pod wait**. Retained diagnostics explicitly show successful rollout and a remaining `1/1 Running` pod; the wait retained retired pod identities. This is a new observed failure, not proof of the earlier Day 2 incident's cause.
- Fix: retain the deployment rollout wait, remove the redundant all-matching-pod wait, and require every live pod in runtime verification to be Ready and annotated for the expected image. Ignore only pods with a deletion timestamp; empty, all-retiring, unready or wrong-image live sets still fail. Existing CRI/Docker config comparison and HTTP checks remain.
- Verification: five new regression cases pass; shell/Python/workflow validation passes; fresh local redeploy and all four existing runtime observations pass. [Local evidence](../reports/sanitized/day3/rollout-fix-local.json). Hosted correction is next; no green overall workflow is claimed yet.
- Original source/baseline artifact ZIP hashes were verified. Only actual failure diagnostics and passing build/test evidence are promoted; runtime was skipped in the failed hosted job. No application source or app lock changed.

### Rollout correction hosted source verification

Commit `d68686a` / [run 39111621696](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696), source job `117628806917`, passed. Artifact `12130199437` matched official ZIP SHA-256 `7e96dff369e214e2c3dd5def98413015a92d278d785a01fc70e949541d3362b7`; all 221 identities/content bindings match local evidence with 186 exact accepted risks and zero blockers/errors. Source-log/artifact privacy checks passed. Baseline job `117628807146` is running the selected application tests; the workflow includes all five new rollout regression cases. Deployment/runtime correction is not yet claimed verified in CI.

## Day 3 completed — 18 October 2026

- Outcome: **all six PF-D3 tasks are complete**. [Run 39111621696](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696), code `d68686a`, passed both jobs: 25 gate contracts, five rollout regressions, actual scanner fixtures/collection/gate, six application install/build/test stages, source image, deployment, runtime and cleanup. Both downloaded artifact ZIP hashes were verified; source identities/content bindings match local data and job-log/artifact privacy checks passed.
- Gate: **221 visible findings, 186 exact approved lab risks, zero blockers/errors**. Approval expires **25 October 2026 at 00:00 IST**; new/changed findings, expiry or scanner failures block. These findings are not marked fixed.
- Actual fix: removed the redundant pod-snapshot wait after rollout; runtime requires live pods Ready and bound to the expected image annotation plus actual CRI/Docker config. The successful hosted run encountered **one terminating pod**, ignored it correctly and passed all four runtime checks. Retained the prior failed-run evidence and the earlier Day 2 incident's unconfirmed-cause limitation.
- Records: synchronized guide/JIRA ticks, setup handoff, Day 2/3 checkpoints, exact review record, versions, requirements, report outline, README and checksum/evidence links. Implementation `d68686a` is published on `feature-16-kick-start`; this closeout carries the final evidence records. Imported source/app locks and system settings remain unchanged.
- Next/blocker: Day 4 hardening checklist remains **unchecked and unstarted**. The program acknowledgement is not completed; the user requested help and its LMS page link is needed. No personal attestation/signature is fabricated. Full IaC/image/DAST gates, AI work, three remediation PRs and rendered final report remain pending.

## Day 4 start request — 19 October 2026

- Request: start Day 4. Read the guide, completed Day 3 evidence and existing hardening checklist; preserved the clean feature branch at `993f1df`.
- Actions: performed read-only environment preflight and created [day4-checkpoint.md](day4-checkpoint.md). Node/npm/Python and Python dependency validation passed; both application locks match; Docker is reachable; the existing kind node is Ready and the baseline deployment has one ready replica. Approximately 570 GiB disk remains. No new HTTP/application/scanner run is claimed.
- Environment drift: both temporary bridge-filter sysctl paths are absent and Docker reports both disabled; IPv4 forwarding remains 1. The cluster's Ready status does not establish fresh network acceptance. No host change was attempted. Checkov/Syft are absent from the selected project PATH.
- Entry condition: the guide explicitly requires the program acknowledgement before Day 4 implementation. Its last recorded status is incomplete. Requested actual completion status/date or the program/LMS link; the start request is not treated as a personal attestation. No signature or sensitive document is recorded.
- Outcome: preflight complete; PF-D4-00 awaits clarification and PF-D4-01 through PF-D4-06 remain unstarted. No scanner installation, hardening, new image, deployment mutation, exception expansion, commit, push or external message occurred. Next: resolve the acknowledgement status, then execute the Day 4 checklist and recheck deployment prerequisites.
- Record verification: `git diff --check` passed; local Markdown link targets resolve across all five changed/new records. Only Markdown files changed; no tests were added for this documentation-only update.

## Connection check — 22 October 2026

- Request/outcome: confirm the assistant is connected and working; chat response and local workspace read/write access are verified.
- Actions/verification: read the setup checkpoint and daily log, preserved existing local changes, and updated these records; `git diff --check` passed for both records.
- Limits/next: external services and application health were not checked. No project implementation resumed; the existing Day 4 entry condition remains pending. Await the next task.

## Resume Day 4 — 22 October 2026

- Request: explain the paused point, resume work, and record the user's confirmation that the Responsible AI acknowledgement is signed.
- Decision: Day 3 remains complete; the acknowledgement confirmation clears PF-D4-00. Confirmation received today; actual signing date was not supplied. No signed material is collected.
- Actions: read the saved handoff/guide, preserved all existing local Markdown changes, rechecked project runtimes and inspected the owned lab. Several current pods are unready despite the node reporting Ready; fresh runtime health is not assumed.
- Completed: isolated Checkov 3.3.30 (100 hash-pinned distributions), verified Syft 1.55.0, added strict custom image-digest policy and eight real CLI fixtures. Built a separate project Dockerfile using retained app locks, pinned Node/distroless bases, explicit build and production-only runtime dependencies. App source/locks remain unchanged.
- Runtime: caught and corrected the app's required CSAF metadata write by adding a bounded writable mount; application code/seed remain read-only. Docker and the Ready hardened Kubernetes deployment each pass seven functional/training checks plus UID/GID 65532, zero capability sets, seccomp, no-new-privileges, root-write denial, explicit writable-directory and token-absence checks. Registered/verified a canonical digest name in local containerd; no registry publication.
- Lab action/limit: retained private startup/events/kubelet diagnostics and restarted only the owned kind node's kubelet service. No host module/sysctl or unrelated workload changed. Current app is Ready with zero restarts; several existing system pods remain unready and the historical cause is not established. No full-cluster recovery is claimed.
- Scans: seven collection stages complete without operational errors. Both immutable image IDs use one frozen DB. Kubernetes failures 15→1; Dockerfile failures 2→0. Image identities 101→100, one unknown CA-certificate advisory removed, zero added; 11 critical and 27 high remain. Syft's 2,748-component CycloneDX 1.6 inventory validates against hash-pinned official schemas and representative installed packages. Raw reports/SBOM stay ignored/private.
- Gate: 15 fail-closed contracts and five existing rollout regressions pass. Actual Day 4 gate exits 1 with **39 blockers and zero operational errors**: one NetworkPolicy control plus 38 image risks. Existing source approvals are byte-unchanged and no Day 4 exception is activated. Bounded CIS 2.0.0 mapping/gaps and a concrete private residual-risk packet are recorded.
- Outcome/next: PF-D4-00 through PF-D4-05 have local evidence; PF-D4-06 comparison/gate evidence exists but security acceptance is open. Resolve/review residual risks and network isolation, then Day 5 DAST/full-pipeline integration. Existing local work was preserved. No commit, push, hosted Day 4 run, live model call or new full application-suite result is claimed. Final Markdown/privacy/whitespace verification is recorded with the evidence index.

- Final verification: eight policy fixtures, 15 gate contracts, five rollout regressions, Python/Node syntax and project dependency validation passed. Both lock comparisons and source/lock/approved-exception Git diffs are clean. Changed Markdown local links/contact checks and `git diff --check` pass; Gitleaks reports zero findings in the reviewed changed-file snapshot. [Validation record](../reports/sanitized/day4/validation.json). Only the intended local implementation/evidence/docs are changed; no staging, commit or push occurred.

## Complete assignment; defer security findings — 22 October 2026 (in progress)

- Request/decision: the user explicitly instructed recording critical/high findings for later remediation and continuing all remaining assignment stages. Security findings no longer stop owned-lab execution. This supersedes the prior Day 4 acceptance stop; it does not change finding severity or establish remediation/production safety.
- Actions: preserved strict evidence, introduced an explicit study-lab execution profile, and started Day 5 DAST/full-pipeline implementation. Existing local work is preserved. Operational errors/missing evidence remain distinct from vulnerabilities.
- Dependencies: asked for provider/model and maximum API spend for the genuine live triage deliverable; continuing mock/local implementation independently. Genuine human review and hosted publication evidence will be recorded only when performed.
- Next: execute ZAP, integrate all scan stages, normalize/deduplicate findings, add measured dashboard and redaction/grounding tests, implement safe triage/patch adapters, and prepare reproducible report/demonstration artifacts. No future-stage completion is asserted in advance.

### Provider options requested during execution

- Request: list available AI choices so the user can select. Checked current official model/pricing documentation for OpenAI, Google and Anthropic and presented three low-cost choices with explicit proposed caps.
- Decision/status: recommended GPT-6 Luna with a proposed $1 application cap; free-tier-only Gemini and Haiku 5.5 with a proposed $1 cap are alternatives. No selection, spend authorization or account access is assumed. [Configuration record](ai-configuration.md).
- Verification/next: official pages were fetched; account-specific availability and credentials remain unverified. Independent local project work continues while selection is pending.

### Existing editor token reuse question

- Request/outcome: asked whether the existing editor API token can be reused. Confirmed that a normal API credential may be reusable, while an editor account sign-in token is a separate credential type.
- Actions/verification: checked only known configuration files and credential/provider-field presence; found an Anthropic-compatible credential/custom endpoint available to the session. No secret value or endpoint address was printed, copied to project files or sent to a new service. No paid/model request was made.
- Next: target the existing compatible integration, verify its behavior/pricing and live limit, and complete pre-egress tests while independent pipeline work continues. A public provider price is not assumed to apply to a custom endpoint.

### OpenAI credential selection and correction

- Requests: the user supplied the location of an existing OpenAI token file, then explicitly corrected the provider choice to OpenAI only.
- Decision/actions: use that external file at runtime, official OpenAI API origin, GPT-6 Luna and the proposed $1 total application cap. Anthropic credentials/custom endpoints are excluded. No token content is copied into project records or displayed.
- Verification/next: read-only model-access validation is being attempted without a generation request; complete captured-body redaction/grounding tests before any real triage call. Remaining local pipeline work continues.

### No new API purchase

- Request/decision: the user declined buying additional API credit. No purchase/top-up/billing change is authorized or performed. Clarified that the proposed $1 was an application usage ceiling, not a required purchase.
- Next: use only the specified OpenAI token and existing available credit for a small bounded evaluation after safeguards; continue independent implementation regardless of account-credit availability. No live result is assumed.

### Remaining stages implemented and locally exercised

- Day 5: added pinned ZAP 2.17.0 baseline scanning inside the owned node's private network namespace, loopback-only API access and route capture. Resolved IPv6-loopback/Host-header allowlist mismatches from retained diagnostics; a real run reached 121 URLs and retained 14 alert groups. Findings are deferred; the scanner container was removed.
- Added six separate hosted scan jobs plus build/test and an authoritative aggregate gate, exact image archive/config verification, read-only PR permissions and sanitized-only scanner receipts. actionlint passed. The complete local execution `20261022T145253045022Z` passed all stages in 115.75 seconds after explicit reuse of a fresh build/test; no hosted execution is yet claimed.
- New online application run had six external-service DNS failures. The explicit offline profile excludes the nine-test internet-resource availability suite, then all six stages pass: 2,326 application tests passed, seven upstream skips, zero failures. Retained the failed online evidence; source and locks remain unchanged.
- Day 6: implemented schema-checked normalization, cross-stage issue deduplication with provenance, public dashboard/JSON/CSV and a post-hoc 21-case curated label set. A real non-executed authorization fixture is missed by the authored SAST patterns. Metrics: TP14/FP0/FN1/TN6, recall 93.3%; no general coverage or independent-label claim. Current data: 372 observations, 235 underlying issues (11 critical, 109 high); all are in the deferred register.
- Days 7–8: 58 tests pass across normalization, aggregate/error/skip contracts, actual captured-body redaction, zero-call refusal, grounding and bounded patch adapters. OpenAI model lookup succeeded, but all three bounded real generation attempts returned HTTP429. No successful live triage, invoice cost or external-API-generated patch is claimed; no further automatic calls/top-ups/purchases. Twenty-finding mock triage validates and remains labeled mock.
- Day 9: three actual Codex-authored local templates address legacy baseline token mounting, non-root policy and liveness. Each selected Checkov check fails before and passes after; isolated Ready deployments pass home/product HTTP checks before and after; all three namespaces are deleted. Draft PR creation and genuine human review remain pending.
- Day 10: authored project-local bootstrap and uniquely named ephemeral-cluster reproduction; report tooling is isolated. Fresh-clone execution, report rendering/visual QA, final privacy review and delivery remain in progress. [Current completion record](project-completion.md).

### No additional purchase; final delivery preparation

- Request reaffirmed: no additional API credit purchase. No purchase, top-up or billing change was made; the three real HTTP429 attempts exhaust automatic retries. Continue local work.
- Verification: project-local bootstrap passed; fresh-catalog tests verify current hash-bound evidence without historical private state and reject tampered raw data. All 60 current tests pass. actionlint and Bash syntax checks pass.
- Actions: generated a twelve-page study PDF, rendered every page and inspected page order/overflow; authored reproduction, genuine-review ledger and defense notes. The automatic study workflow defers findings while retaining execution errors; the strict historical workflow is manual. Fresh clone execution and draft PR publication remain in progress.

### Publication and clean-checkout regression

- Published integration commit `37ff4c1` and created three independent focused draft remediation PRs; see the review ledger. No approval, reviewer message or merge occurred.
- The first hosted SCA job exposed a real clean-checkout bug: retained locks were not restored before the standalone scan. Added missing-lock restoration while preserving/refusing changed local locks, removed stale stage receipts before collection and added two regression tests. All 62 current tests pass.
- Fresh clone bootstrap encountered a stalled default-IP download; IPv4 access returned HTTP200, so bootstrap downloads now select IPv4. This is a download transport correction, not a host-network setting change. Fresh execution remains in progress.
