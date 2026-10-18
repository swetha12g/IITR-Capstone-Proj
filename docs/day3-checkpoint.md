# Day 3 checkpoint — scans implemented, baseline owner review pending

Started **18 October 2026 (Asia/Kolkata)**, synchronized with [the execution guide](../10-days-work-break-down.md) and [daily JIRA board](daily-log.md).

## Current acceptance

- [x] Three pinned scanners execute; full-history and working-tree secret scans run.
- [x] Reports, finding/operational exit codes and coverage are validated locally.
- [ ] Exact expiring baseline risks accepted by the designated reviewer.
- [x] Real scanner bad/fixed demonstrations pass expected outcomes.
- [x] Missing/invalid reports, crashes, timeouts, skips and expired exceptions fail closed.
- [ ] Final hosted evidence/privacy cross-check for the corrected dependency scope.

## Current verified local results

Semgrep CE 1.181.0, Trivy 0.76.0 and Gitleaks 8.30.1 are isolated under ignored `.tools/day3/`. Official distribution hashes were verified; all 66 Semgrep Python distributions are hash-pinned. No system tools, shell startup, bridge settings or imported application bytes were changed. [Tool pins](../locks/scanners/tools.json), [verification](../reports/sanitized/day3/tools-verification.json), [versions](versions.md).

Semgrep scanned 643 JavaScript/TypeScript files, producing 11 matches and zero parser errors. Twelve exact upstream lesson fragments that are not standalone TypeScript units are excluded with file hashes/reasons in [coverage exclusions](../policies/semgrep/coverage-exclusions.json); other source and tests remain included. Rules are local with telemetry/version checks disabled and no account or remote rule fetch.

Trivy explicitly scans **production and development** dependencies from both recorded lockfiles. It reports 74 raw rows (42 high/critical), collapsing two duplicate identities to 72 distinct dependency findings. Gitleaks reports 69 history and 69 working-tree matches; all 24 match files equal the public upstream pin, with history introductions in the verified source-import commit. This establishes provenance, not credential safety. No match values, raw lines or author contacts are published.

The current gate has **221 distinct findings and 186 blocking risks**, with zero operational errors. [Gate result](../reports/sanitized/day3/gate-summary.json), [current owner review packet](day3-baseline-review.md), [186 exact proposals](../reports/sanitized/day3/baseline-review-proposals.json). **Active exceptions remain empty.** The earlier 183-entry production-only request is superseded; any approval naming only those entries cannot authorize the additional findings.

All **25** local contract tests passed, including coverage declaration, crashes/timeouts, malformed/missing/stale reports, strict parser coverage, shallow history, missing/skipped stages, exact exception identity, expiry, severity changes, source/lock-file content binding, fixture separation and exclusion of raw match/contact fields. [Tests](../reports/sanitized/day3/gate-tests.json).

Actual scanner fixtures detected all six source patterns, `CVE-2021-23337` in lodash 4.17.20 and a generated nonfunctional token-shaped canary. Fixed source, lodash 4.18.1 and a clean tree/history passed with zero findings. A separate committed-canary probe stayed blocked after working-tree removal. [Fixture evidence](../reports/sanitized/day3/fixture-evidence.json), [official advisory](https://github.com/advisories/GHSA-35jh-r3h4-6jhm). No fixture is executed or deployed, and no real credential is validated.

## Hosted history and coverage correction

Initial code `1dad4b7` was normally pushed. [Run 39107551251](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39107551251), source job `117616578672`, passed verified tool installation, 24 then-current contracts, actual fixtures and collection. Its gate correctly failed on 183 unapproved risks, with no operational error. The parallel baseline job passed its application build/tests, image, cluster deployment, runtime and cleanup. That run used Trivy's production-only default and is **not final verification of the expanded source scope**.

Downloaded artifact `12128659514` matched SHA-256 `94cbf4f7b27904c430d575ba4c4508bbe7dd9f0af4554524f2594e5d830af5bd`; all 217 then-current identities and bindings matched local evidence. It contained no raw match/contact fields or generated canary. [Historical CI record](../reports/sanitized/day3/ci/gate-summary.json). The development-dependency omission was then corrected locally, adding three high findings and a coverage contract test; a fresh hosted verification is required.

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
