# Day 3 checkpoint — scans implemented, baseline owner review pending

Started **18 October 2026 (Asia/Kolkata)**, synchronized with [the execution guide](../10-days-work-break-down.md) and [daily JIRA board](daily-log.md).

## Current acceptance

- [x] Three pinned scanners execute; full-history and working-tree secret scans run.
- [x] Reports, finding/operational exit codes and coverage are validated locally and in CI.
- [ ] Exact expiring baseline risks accepted by the designated reviewer.
- [x] Real scanner bad/fixed demonstrations pass expected outcomes.
- [x] Missing/invalid reports, crashes, timeouts, skips and expired exceptions fail closed.
- [x] Hosted source evidence/privacy cross-check for the corrected dependency scope.

## Current verified local results

Semgrep CE 1.181.0, Trivy 0.76.0 and Gitleaks 8.30.1 are isolated under ignored `.tools/day3/`. Official distribution hashes were verified; all 66 Semgrep Python distributions are hash-pinned. No system tools, shell startup, bridge settings or imported application bytes were changed. [Tool pins](../locks/scanners/tools.json), [verification](../reports/sanitized/day3/tools-verification.json), [versions](versions.md).

Semgrep scanned 643 JavaScript/TypeScript files, producing 11 matches and zero parser errors. Twelve exact upstream lesson fragments that are not standalone TypeScript units are excluded with file hashes/reasons in [coverage exclusions](../policies/semgrep/coverage-exclusions.json); other source and tests remain included. Rules are local with telemetry/version checks disabled and no account or remote rule fetch.

Trivy explicitly scans **production and development** dependencies from both recorded lockfiles. It reports 74 raw/distinct dependency findings (42 high/critical). Gitleaks reports 69 raw rows per history/tree scan, representing 68 distinct locations in each; all 24 match files equal the public upstream pin, with history introductions in the verified source-import commit. This establishes provenance, not credential safety. No match values, raw lines or author contacts are published.

The current gate has **221 distinct findings and 186 blocking risks**, with zero operational errors. [Gate result](../reports/sanitized/day3/gate-summary.json), [current owner review packet](day3-baseline-review.md), [186 exact proposals](../reports/sanitized/day3/baseline-review-proposals.json). **Active exceptions remain empty.** The earlier 183-entry production-only request is superseded; any approval naming only those entries cannot authorize the additional findings.

All **25** local contract tests passed, including coverage declaration, crashes/timeouts, malformed/missing/stale reports, strict parser coverage, shallow history, missing/skipped stages, exact exception identity, expiry, severity changes, source/lock-file content binding, fixture separation and exclusion of raw match/contact fields. [Tests](../reports/sanitized/day3/gate-tests.json).

Actual scanner fixtures detected all six source patterns, `CVE-2021-23337` in lodash 4.17.20 and a generated nonfunctional token-shaped canary. Fixed source, lodash 4.18.1 and a clean tree/history passed with zero findings. A separate committed-canary probe stayed blocked after working-tree removal. [Fixture evidence](../reports/sanitized/day3/fixture-evidence.json), [official advisory](https://github.com/advisories/GHSA-35jh-r3h4-6jhm). No fixture is executed or deployed, and no real credential is validated.

## Hosted history and coverage correction

Initial code `1dad4b7` was normally pushed. [Run 39107551251](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39107551251), source job `117616578672`, passed verified tool installation, 24 then-current contracts, actual fixtures and collection. Its gate correctly failed on 183 unapproved risks, with no operational error. The parallel baseline job passed its application build/tests, image, cluster deployment, runtime and cleanup. That run used Trivy's production-only default and is **not final verification of the expanded source scope**.

Downloaded artifact `12128659514` matched SHA-256 `94cbf4f7b27904c430d575ba4c4508bbe7dd9f0af4554524f2594e5d830af5bd`; all 217 then-current identities and bindings matched local evidence. It contained no raw match/contact fields or generated canary. [Historical CI record](../reports/sanitized/day3/ci/gate-summary.json). The development-dependency omission was then corrected locally, adding three high findings and a coverage contract test; the corrected scope was verified by the later run below.

## Reproduce

```bash
source scripts/dev-env.sh
python scripts/install-scanners.py
python scripts/test-day3-gates.py
python scripts/verify-day3-fixtures.py
bash scripts/scan.sh
python scripts/gate.py --manifest "$(cat reports/private/day3/latest-manifest.txt)" \
  --profile day3 --output reports/sanitized/day3/gate-summary.json
```

Collection captures each stage separately and continues after findings/errors. Semgrep finding exit is 1; Trivy/Gitleaks use explicit finding exit 20. Raw report hashes, schemas and operational status are checked separately by the gate. Ignored application lock copies must match tracked locks; mismatches are preserved and rejected. Current-file exceptions bind SHA-256 content, rule/path/location or package/advisory/version, severity, owner role, baseline commit and expiry. Historical identities also bind the immutable Git commit. No blanket passing error suppression or wildcard exception exists.

The tree scan copies tracked and non-ignored untracked files, refusing symlinks instead of following external paths. Tools use isolated HOME/settings/Docker configuration; ignored private reports/environments/dependency trees and credential files are not copied. Full history uses all fetched refs; CI checkout uses `fetch-depth: 0`.

The complete `full` profile still blocks on missing IaC, container and DAST reports. This Day 3 gate is not full capstone acceptance or production safety. Day 4 acknowledgement and later live-AI budget/model prerequisites remain separate; Day 4 has not started.

## Corrected hosted source result

[Run 39108322664](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39108322664), code `421f8eb`, source job `117618870374`, passed scanner installation, **25** contracts, live bad/fixed fixtures and all collection with production/development coverage. Its gate correctly exited 1 on **186 unapproved risks**, zero operational errors; the gate is not reported as passing. The parallel baseline job completed successfully, including application build/tests, image deployment, runtime and cleanup.

Downloaded artifact `12129287626` matched SHA-256 `16a6749e2cf91180a5b2cbccee34dde19146875949a3d302b37d95a3b7faa5e9`. All **221** finding identities and content bindings match local evidence. [Current CI gate](../reports/sanitized/day3/ci/39108322664/gate-summary.json), [tests](../reports/sanitized/day3/ci/39108322664/gate-tests.json), [execution](../reports/sanitized/day3/ci/39108322664/scan-execution.json). Sanitized artifacts and the full source-job log passed checks for raw match/contact fields, credential-shaped canaries and private-key headers.

Remaining Day 3 acceptance dependency: the designated project-owner reviewer must decide on the current **186-entry** packet. No response or elapsed time is treated as approval; active exceptions remain empty. The guide calls for reviewed mappings/precise risk exceptions and states that completion claims need actual tests, artifacts and human review; the reviewer role is recorded in [scope.md](scope.md).

## Technical closeout and remaining decision

The complete run concluded **failure**, solely because the source policy gate rejected 186 unapproved risks. The baseline application job passed; source installation, scans, 25 tests, live probes and sanitized evidence checks passed. Both source and baseline artifact ZIP hashes were verified after download; [CI receipt](../reports/sanitized/day3/ci-receipt.json), [baseline build/tests](../reports/sanitized/day3/ci/39108322664/baseline/build-tests.json), [baseline runtime](../reports/sanitized/day3/ci/39108322664/baseline/runtime-baseline.json).

Five of six PF-D3 tasks are verified; PF-D3-03 remains pending the designated owner's explicit decision on [the 186-entry packet](day3-baseline-review.md). The active exception list is empty. No human acceptance is invented and no failing gate is waived. Day 3 is **not claimed complete** while this review is pending. No independent approval, production safety, full six-stage pipeline, rendered final report or live-AI result is claimed. Day 4 remains unstarted.

Implementation `421f8eb` is published to `feature-16-kick-start`; documentation/evidence closeout follows with the review item still open. No application source/recorded app locks, shell startup, global Git settings or persistent bridge settings changed.

### Count-label correction and publication

The authoritative JSON has 11 SAST + 74 dependency + 68 history + 68 tree identities = 221. Blocking identities are 8 + 42 + 68 + 68 = 186. Each secret scanner report has 69 raw rows, with one repeated location identity; the dependency report has no such duplicate. Earlier prose assigned the two duplicates to the wrong stage; those labels are corrected. The 186 proposal fingerprints, content bindings and approval scope did not change.

Documentation/evidence closeout `7c876e0` was normally pushed; ahead/behind counts were `0 / 0` and the tree was clean at delivery verification. A final count/receipt correction follows, with no tested code change and no baseline approval invented.
