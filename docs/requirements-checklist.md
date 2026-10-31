# Requirements and acceptance checklist

Updated: 23 October 2026. Individual execution scope is recorded in [scope.md](scope.md).

Current critical-remediation variant: zero critical findings in fresh source/image scans, 2,332 selected application passes / six skips, 79 current local contracts, 76 in accepted hosted repair run 39842575944, 25 source contracts, and verified Docker/temporary-Kubernetes/owned-study deployment. Critical repairs are committed/pushed; the repaired b20b9b1 fresh checkout also passed all stages with cleanup. Earlier Day 1–4 statements below retain their historical scope. [Current repair proof](critical-remediation.md).

## Day 1 acceptance

| Requirement | Status | Evidence / limitation |
|---|---|---|
| Correct feature branch and authenticated fetch | Passed | Environment recheck and repository status |
| Source provenance and license | Passed | [upstream-provenance.md](upstream-provenance.md), exact 1,466-file import verification |
| Working Docker daemon | Passed | 27.3.1 reachable; bridge filters enabled; no warnings |
| Supported Node and Python test environment | Passed | [versions.md](versions.md), official checksum and environment checks |
| Application build | Passed | Explicit frontend/server production build; exit 0; outputs verified |
| Selected finite application tests | Passed with recorded skips | Frontend 1,372 passed; server 417 passed / 2 skipped; API 545 passed / 6 skipped; zero failures |
| Private data excluded from publication candidates | Passed for reviewed publication scope | Ignore checks, complete source visibility, lock URL review, new-document privacy and whitespace checks passed. Source-only staging matched the pin plus one ignore override; no private files were staged. No full secrets-scanner verdict is claimed for upstream fixtures |
| Submission/reviewer planning facts | Passed with external dependency noted | Submission 18 October 2026; project owner is manual reviewer; independent approval/coordinator acceptance remains separately pending |

## Day 2 acceptance

Source image, Ready local kind lab, loopback HTTP/screenshot, confirmed runtime baseline, hosted build/tests and actual run URL all passed. [Successful run 38957969793](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38957969793), [CI receipt](../reports/sanitized/day2/ci-receipt.json), [Day 2 checkpoint](day2-checkpoint.md). Earlier deployment failure cause remains unconfirmed because its private log was discarded; later successful evidence is recorded separately. Local manual review was explicitly confirmed; independent PR approval is not claimed.

## Project requirements

| ID | Requirement | Planned stage | Status |
|---|---|---|---|
| PF-ENV | Environment, pinned source, build/test evidence | Day 1 | Passed locally; test skips recorded; user authorized publishing the reviewed packet |
| PF-RUNTIME | Built source image, own kind deployment, local HTTP and confirmed runtime baseline | Day 2 | Passed locally and in hosted CI; reviewed screenshot and three confirmed observations recorded |
| PF-SAST | Semgrep rules, source reports, known bad/fixed gate evidence | Day 3 | Local/hosted execution and six-rule probes passed; 186 exact lab-only risks explicitly approved; fresh local gate passes |
| PF-SCA | Trivy dependency findings and reviewed severity gates | Day 3 / critical repair | Current source scan includes development dependencies: zero critical, ten high. Root lock updated for remediation; earlier exact source approvals remain historical and unchanged |
| PF-SECRETS | Full-history and working-tree scans with safe canary evidence | Day 3 | Local/hosted history/tree scans and canary/history probes passed; 186 exact lab-only risks explicitly approved; fresh local gate passes |
| PF-IAC | Checkov built-in/custom policies and tested controls | Day 4 | Local evidence verified: eight actual CLI fixtures; Kubernetes failures 15→1, Dockerfile failures 2→0; NetworkPolicy control is deferred under the study profile |
| PF-IMAGE | Functional hardened image, exact-image scan, Syft SBOM, selected CIS mappings | Day 4 | Local build, seven Docker/seven Kubernetes checks, exact-image scans and 2,658-component current schema-validated SBOM verified; zero critical / five high image findings after repair; historical Day 4 comparison retained |
| PF-DAST | Pinned ZAP baseline reaches the owned app; limitations recorded | Day 5 | Real pinned passive run reached 121 URLs; route and cleanup proof retained |
| PF-GATES | All six stages, failures/skips fail closed, precise expiring exceptions | Days 3–5 / critical repair | All seven current local receipts and aggregate pass with zero critical; 79 current local contracts and CLI controls verify critical blocking, tree/timing binding and truthful Summary publication. Repair hosted run 39842575944 passed all eight jobs; updated report/dashboard validation is recorded separately |
| PF-METRICS | Normalization, independent labels including misses, reproducible dashboard and detection metrics | Day 6 | Current dashboard: 180 issues / zero critical / 91 high; TP14/FP0/FN1/TN6 on 21 post-hoc cases; independent labeling remains open |
| PF-REDACTION | Source-free allowlisted payloads, captured mock-body checks, refusal means zero calls | Day 7 | Captured-body and zero-call refusal tests pass; independent version grounding and current code/prompt proof retained |
| PF-AI | Explicit budgeted live call after safeguards, grounding, FP/FN and cost/model disclosure | Day 8 | Client and mock complete; model lookup HTTP200; all three generation attempts HTTP429. Successful live evaluation/usage unavailable; no new spending |
| PF-PRS | Three genuine AI-assisted fixes, before/after tests, real independent human review | Day 9 | Three separate coding-assistant draft PRs published, with green hosted workflows; actual before/after scanner/runtime checks and 62 contracts pass; independent human review pending |
| PF-REPORT | 12-page evidence-based report, maturity assessment, fresh reproduction, defense | Day 10 | Twelve-page PDF and evidence packet delivered; two fresh-directory pipelines and a full clean-PATH run passed with cleanup; defense guide authored. Oral assessment remains pending |
| PF-ETHICS | Lab-only scope, confidentiality, acknowledgement before Day 4, GenAI disclosure | Every stage | User confirmed signing on 22 October before resumed implementation; signing date unspecified; no signed material stored; ongoing lab/privacy/AI safeguards still apply |

Day 3 strict source-approval counts refer to the historical dated run; the current study profile retains updated DB findings without widening those exact approvals. Successful live AI, independent labels/review and the oral assessment remain separate evidence requirements.

The 80% detection target must be measured against a labeled introduced set; no success or grade is promised. Optional work waits for core acceptance. Upstream intentionally vulnerable infrastructure is not a deployment template for this project.

## Day 3 historical hosted verdict — before owner approval

[Run 39108322664](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39108322664) verified scanner operation, 25 contracts, real probes and sanitized evidence. Its source gate correctly failed on 186 unapproved risks (zero operational errors); the application build/deployment job passed. [Historical CI receipt](../reports/sanitized/day3/ci/39108322664/receipt.json). At that observation five PF-D3 tasks were verified and baseline owner acceptance remained open. The current explicit owner decision is recorded below; full capstone acceptance remains pending.

### Current owner decision and completed Day 3

The designated reviewer explicitly accepted the current 186 exact lab-only entries on 18 October, expiring 25 October at 00:00 IST. Local and [hosted run 39111621696](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696) gates pass with 221 findings visible, 186 accepted risks, zero blockers/errors; all 25 gate contracts and five rollout regressions pass. The corrected application baseline also passes build/tests, deployment, image identity, four runtime checks and cleanup. [Current receipt](../reports/sanitized/day3/ci-receipt.json). All six PF-D3 tasks are complete. Accepted risks are not fixes. The Day 4 acknowledgement is confirmed. The later study decision defers vulnerabilities; [current delivery status](project-completion.md) distinguishes completed implementation from remaining live/review evidence.

## Critical repair publication verified — 23 October 2026 IST

[Hosted run 39842575944](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) passed all eight jobs on `1616f14`: zero critical, 2,332 selected application passes / six skips, 76 contract passes, lint/snippet checks, schema-valid SBOM, seven runtime checks and passive DAST/cleanup. Detailed Summary and ten-file artifact are published and checksum-verified; [receipt](../reports/sanitized/critical-remediation/ci/verification.json). Earlier new-CI-pending statements describe the preceding local snapshot. High/lower findings and genuine live AI/independent review/oral evidence remain pending as specified above. No new API usage or purchase occurred.

[Requirement-by-requirement Days 5–10 audit](completion-audit.md) records the verified fresh repaired checkout, complete dashboard displays and twelve-page render, while retaining the unfulfilled external assessment evidence.
