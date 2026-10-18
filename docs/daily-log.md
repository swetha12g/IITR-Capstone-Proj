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

- Rerun outcome: changed template rolled out; unchanged-image second apply reported no patch change; runtime recheck passed on the replacement pod. Corrected implementation `c1d78b9` was pushed normally. Final verification is [run 38955433523](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38955433523); awaiting its actual result.

## Next checkpoint backlog — Day 3, planned for 18 October 2026

Day 2 was brought forward to 17 October. Execution started on **18 October 2026** at the user's request. This is the JIRA-style Markdown board, based on the guide's Day 3; no external JIRA issues or scanner installations are created by this plan. Target timebox: 300 minutes. The remaining Days 3–10 still total approximately 40 focused hours, so this board is not a promise of a complete submission on 18 October. Exact cutoff/coordinator interpretation remains unresolved.

| ID | Task | Status | Priority | Estimate | Acceptance criteria |
|---|---|---|---|---|---|
| PF-D3-01 | Verify and pin official Semgrep, Trivy and Gitleaks tools; configure reviewed rules | Done: local and hosted verification | High | 120 min | Official versions/checksums and supported CLI flags recorded; meaningful JS/TS rules and narrow generated/vendor exclusions; application source remains in scope |
| PF-D3-02 | Run source, dependency, full-history and working-tree scans | Done: local and hosted verification | High | 45 min | Private machine-readable output; timestamps/exit codes captured; full Git history fetched in CI; distinguish findings from scanner execution errors |
| PF-D3-03 | Triage baseline and define exact expiring exceptions | Pending owner review: 186 exact entries | High | 15 min | Rule/advisory, component/path fingerprint, reason, owner role, expiry and baseline commit; no blanket application suppression |
| PF-D3-04 | Implement scan wrapper and fail-closed gate policy | Done: local and hosted verification | Highest | 60 min | Explicit severity mappings; invalid/missing JSON, crashes, mandatory skips and expired exceptions block; collect all reports without blanket passing error suppression |
| PF-D3-05 | Prove bad/fixed behavior with isolated synthetic fixtures | Done: local and hosted verification | High | 30 min | Unsafe source pattern, verified advisory fixture and token-shaped canary detected; repaired/removed fixtures pass relevant gates; no real credential or seeded deployed feature |
| PF-D3-06 | Run hosted checks and review sanitized evidence | Done: verified evidence; policy gate blocked | High | 30 min | Actual run URL/results, policy tests, JSON validation and baseline risk visible; no raw secret matches in public output; update requirements/report/evidence |

- [x] PF-D3-01 — official tool pins and reviewed scanner configuration.
- [x] PF-D3-02 — three scanners execute with valid private reports, full history and working-tree coverage.
- [ ] PF-D3-03 — precise reviewed baseline exceptions.
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
