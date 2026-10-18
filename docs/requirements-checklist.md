# Requirements and acceptance checklist

Updated: 17 October 2026. Individual execution scope is recorded in [scope.md](scope.md).

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

## Remaining project requirements

| ID | Requirement | Planned stage | Status |
|---|---|---|---|
| PF-ENV | Environment, pinned source, build/test evidence | Day 1 | Passed locally; test skips recorded; user authorized publishing the reviewed packet |
| PF-RUNTIME | Built source image, own kind deployment, local HTTP and confirmed runtime baseline | Day 2 | Passed locally and in hosted CI; reviewed screenshot and three confirmed observations recorded |
| PF-SAST | Semgrep rules, source reports, known bad/fixed gate evidence | Day 3 | Local/hosted execution and six-rule probes passed; exact baseline owner review pending |
| PF-SCA | Trivy dependency findings and reviewed severity gates | Day 3 | Local/hosted production+development reports and real advisory probe passed; high/critical baseline owner review pending |
| PF-SECRETS | Full-history and working-tree scans with safe canary evidence | Day 3 | Local/hosted history/tree scans and canary/history probes passed; exact baseline owner review pending |
| PF-IAC | Checkov built-in/custom policies and tested controls | Day 4 | Pending |
| PF-IMAGE | Functional hardened image, exact-image scan, Syft SBOM, selected CIS mappings | Day 4 | Pending |
| PF-DAST | Pinned ZAP baseline reaches the owned app; limitations recorded | Day 5 | Pending |
| PF-GATES | All six stages, failures/skips fail closed, precise expiring exceptions | Days 3–5 | Source gate and 25 fail-closed contracts implemented; baseline review pending; full profile blocks on missing later stages |
| PF-METRICS | Normalization, independent labels including misses, reproducible dashboard and detection metrics | Day 6 | Pending |
| PF-REDACTION | Source-free allowlisted payloads, captured mock-body checks, refusal means zero calls | Day 7 | Pending |
| PF-AI | Explicit budgeted live call after safeguards, grounding, FP/FN and cost/model disclosure | Day 8 | Pending |
| PF-PRS | Three genuine AI-assisted fixes, before/after tests, real independent human review | Day 9 | Pending |
| PF-REPORT | 12-page evidence-based report, maturity assessment, fresh reproduction, defense | Day 10 | Pending |
| PF-ETHICS | Lab-only scope, confidentiality, acknowledgement before Day 4, GenAI disclosure | Every stage | In progress; acknowledgement pending |

The 80% detection target must be measured against a labeled introduced set; no success or grade is promised. Optional work waits for core acceptance. Upstream intentionally vulnerable infrastructure is not a deployment template for this project.

## Day 3 current verdict — baseline review pending

[Run 39108322664](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39108322664) verified scanner operation, 25 contracts, real probes and sanitized evidence. Its source gate correctly failed on 186 unapproved risks (zero operational errors); the application build/deployment job passed. [CI receipt](../reports/sanitized/day3/ci-receipt.json). Five PF-D3 tasks are verified; baseline owner acceptance remains open, so Day 3 and the full capstone are not declared complete.
