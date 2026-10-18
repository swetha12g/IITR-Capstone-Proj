# Day 3 checkpoint — source scans and regression gates

Started **18 October 2026 (Asia/Kolkata)** at the user's request, following Day 3 in [the execution guide](../10-days-work-break-down.md) and the [daily JIRA backlog](daily-log.md).

## Current state

- Clean `feature-16-kick-start` checkout preserved; authenticated fetch passed and ahead/behind counts were `0 / 0`.
- Repository has full Git history. Project Python 3.10.12, Node 24.22.0 and Docker 27.3.1 are available; approximately 573 GiB disk free at recheck.
- Official release information checked: Semgrep 1.181.0, Trivy 0.76.0 and Gitleaks 8.30.1. Isolated installation passed: official Trivy/Gitleaks checksums verified, Semgrep wheel matched PyPI, and all 66 Python distributions are hash-pinned.
- Raw reports and logs go under ignored `reports/private/day3/`. Tools go under ignored `.tools/day3/`; no system installation or credential inspection is required.

## Acceptance

- [x] Three pinned scanners execute; full-history and working-tree secret scans run.
- [x] Machine-readable reports and operational exit codes validated.
- [ ] Exact expiring baseline exceptions reviewed; no blanket suppression.
- [x] Real bad/fixed scanner demonstrations pass their expected outcomes.
- [x] Missing/invalid reports, crashes, skips and expired exceptions fail closed.
- [ ] Hosted evidence and sanitized records verified; no raw secret match published.

The Day 3 gate covers SAST, SCA and secrets only. IaC/image/DAST stages and the complete six-stage aggregate remain pending later guide checkpoints. Existing intentional training findings are not automatically accepted. Day 4 acknowledgement and live-AI budget/model prerequisites remain separate; Day 4 is not started here.

## Verified local results

Semgrep: 11 matches, 643 scanned JavaScript/TypeScript files and zero parser errors after excluding 12 exact upstream lesson fragments that are not standalone TypeScript units. Their file hashes/reasons are in [coverage-exclusions.json](../policies/semgrep/coverage-exclusions.json); other source/tests remain in scope and imported bytes are unchanged. Rules are local, with no account, remote rule fetch, telemetry or version check.

Trivy: 70 raw rows (39 high/critical); two duplicate identities collapse to 68 distinct dependency findings. Gitleaks: 69 history and 69 working-tree matches, all in 24 byte-identical public upstream files; history matches originate from the verified source import. Raw values/lines/contact metadata are not included in public evidence. This is provenance evidence, not proof that a credential is safe.

The gate reports 217 distinct fingerprints and **183 blockers** before exception review. [Owner review packet](day3-baseline-review.md) and [exact pending entries](../reports/sanitized/day3/baseline-review-proposals.json) are prepared; the active exception file is empty. No acceptance has been fabricated.

All 24 gate contract tests passed, including real child-process crash/timeout capture, malformed/missing/stale reports, strict parser coverage, shallow history, missing/skipped stages, exact exception identity, expiry, severity escalation, fixture-vs-application separation and exclusion of raw match/contact fields. [Gate tests](../reports/sanitized/day3/gate-tests.json).

Real scanner fixtures detected all six source patterns, `CVE-2021-23337` in lodash 4.17.20 and a generated nonfunctional GitHub-shaped canary. Fixed source, lodash 4.18.1 and a clean tree/history passed with zero findings. A separate committed-canary probe remained blocked after working-tree removal, proving history was not silently erased. [Fixture evidence](../reports/sanitized/day3/fixture-evidence.json). No fixture source is executed or deployed. The [official advisory](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) verifies the selected bad-version/repair boundary.

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

The collector captures each exit separately, runs remaining scanners after a finding/error and stores reports/logs privately. Semgrep findings exit 1; Trivy/Gitleaks findings use explicit exit 20. Operational exits/timeouts/missing reports block. The separate gate checks raw report hashes and shape; no blanket passing error suppression is used. Ignored application lock copies must match tracked recorded locks; mismatches are preserved and rejected.

The working-tree secret scan uses a snapshot of tracked and non-ignored untracked files, refusing symlinks instead of following paths outside the repository. Home/tool configuration is isolated. Private reports, environments, dependency trees and credential files ignored by Git are not copied. Full-history scanning uses all fetched refs, and CI checks out with `fetch-depth: 0`.

The `full` profile still requires IaC, container and DAST reports and blocks until they are implemented. The Day 3 profile is not a full capstone or production-safety verdict. Hosted verification and owner baseline review remain pending.
