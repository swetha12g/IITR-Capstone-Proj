# Day 3 checkpoint — complete with exact lab-risk acceptance

Updated **18 October 2026 (Asia/Kolkata)**; synchronized with [execution guide](../10-days-work-break-down.md) and [daily JIRA board](daily-log.md).

## Current acceptance

- [x] Three pinned scanners execute; full-history and working-tree secret scans run.
- [x] Reports, execution codes and production/development coverage validated locally and in hosted CI.
- [x] Designated project-owner reviewer explicitly accepted the current 186 exact lab-only entries.
- [x] Real scanner bad/fixed/history demonstrations verified.
- [x] All 25 fail-closed contracts pass, including expiry and content changes.
- [x] Hosted evidence/privacy cross-check verified.
- [x] Fresh hosted source gate after enabling the approved exceptions.

## Verified current result

The fresh local application gate **passes**: **221 visible findings, 186 accepted baseline risks, zero blockers and zero operational errors**. The approval expires **25 October 2026 at 00:00 IST**. New identities, changed severity/source/lock contents, expiry, missing reports or scanner failures still block. [Gate](../reports/sanitized/day3/gate-summary.json), [review receipt](../reports/sanitized/day3/owner-review.json), [active exact exceptions](../policies/baseline-exceptions.json). No blanket suppression or source change was made.

The user explicitly accepted the updated 186-entry packet and requested study/experimental use and finding fixes. Acceptance is **not remediation**: the findings remain visible. The next guide stage addresses image/Kubernetes hardening with before/after checks; three independently scoped source/dependency/configuration remediation PRs belong to Day 9 and require their own regression/scanner evidence. No application or dependency fix is claimed here.

Semgrep CE 1.181.0 scanned 643 JS/TS files: 11 findings, zero parser errors. Twelve exact partial lesson fragments have documented hash-bound exclusions; runtime source and tests remain covered. Trivy 0.76.0 includes production/development dependencies: 74 distinct findings (42 high/critical). Gitleaks 8.30.1 found 69 raw rows / 68 distinct locations in each history/tree scan. All 24 affected files match the public upstream pin; provenance does not establish credential safety. Raw match values remain private. Tool distributions/66 Python dependencies are hash-pinned under isolated ignored tooling.

Unique stage counts: **11 + 74 + 68 + 68 = 221**; approved blocking identities: **8 + 42 + 68 + 68 = 186**. All **25** local gate contracts passed again after approval. Actual scanner probes previously verified all six source rules, a reviewed lodash advisory and a generated nonfunctional canary; repaired fixtures passed and a removed historical canary still blocked. [Tests](../reports/sanitized/day3/gate-tests.json), [fixtures](../reports/sanitized/day3/fixture-evidence.json). Synthetic probes are not fixes to deployed Juice Shop.

## Hosted history

- Production-only run [39107551251](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39107551251), code `1dad4b7`: expected 183-risk gate rejection, application baseline passed. Superseded by development coverage correction.
- Corrected run [39108322664](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39108322664), code `421f8eb`: tools, 25 contracts, live probes and all scans passed. Gate correctly failed on **186 then-unapproved risks**, zero operational errors; the application build/tests/image/deployment/runtime/cleanup passed. Downloaded source/baseline artifacts matched official ZIP SHA-256. All 221 CI identities/content bindings matched local evidence, with published metadata/log privacy checked. [Historical source gate](../reports/sanitized/day3/ci/39108322664/gate-summary.json). That historical failure remains unchanged.
- Approval-policy commit `c88ec1f`: [run 39110505372](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39110505372), source job `117625451381` **passed**. Verified downloaded artifact `12130745314` ZIP SHA-256 `85c2a6d575759246afc00576dfb2ec176755a93a80dfb8ab805d324bdc5f03f3`: 25 contracts pass, actual probes pass, all 221 identities/content bindings equal local evidence, 186 accepted risks, zero blockers/errors. The parallel baseline failed after a successful rollout: the redundant label-wide wait timed out on retiring pod snapshots. Its final diagnostics showed the live pod `1/1 Running`. A narrow deployment/runtime selection fix passed five regression cases and a fresh local redeploy with all four runtime checks; hosted correction is in [run 39111621696](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696), code `d68686a`. Its source job `117628806917` passed, with the same exact 221 identities and 186 approvals; the corrected baseline job also passed deployment, runtime and cleanup; final evidence is below.

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


## Next step and limitations

Day 3 is complete for its defined source-scan/gate scope; all six PF-D3 tasks are checked. Day 4 has not started: the guide requires Responsible AI Use and Lab Conduct acknowledgement before that stage; the user reported it is not completed and requested assistance. The program/LMS page link has been requested to help; no signature or completion is fabricated and any signed record stays private. The full profile still rejects missing IaC, container and DAST stages. No production readiness, independent GitHub approval, full capstone, live-AI result or rendered final report is claimed. System Node, shell startup, global Git configuration, persistent bridge settings, imported source and recorded app locks remain unchanged.

## Final verified closeout — 18 October 2026

[Run 39111621696](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696), code `d68686a`, completed **success**. Source job `117628806917` and baseline job `117628807146` both passed. Source: 25 contracts, actual scanner probes, production/development collection and the gate (221 visible / 186 exact accepted / zero blockers/errors). Baseline: five rollout regression cases, six application install/build/test stages, source image, kind deployment, actual image identity, four runtime checks and cleanup all passed. **One terminating pod was present and correctly excluded in the successful hosted runtime check**; every live pod was Ready and matched the expected image. This directly exercises the correction, without weakening readiness or hiding a live-pod failure.

Downloaded source artifact `12130199437` matched ZIP SHA-256 `7e96dff369e214e2c3dd5def98413015a92d278d785a01fc70e949541d3362b7`; baseline artifact `12130564571` matched `dba4c58132054b52235643f998d85dcb189eda274adbc25e869089f77b307a4a`. Source identities/content bindings match local evidence; both job logs and published metadata passed privacy checks. [Receipt](../reports/sanitized/day3/ci-receipt.json), [source gate](../reports/sanitized/day3/ci/39111621696/gate-summary.json), [baseline tests](../reports/sanitized/day3/ci/39111621696/baseline/build-tests.json), [runtime](../reports/sanitized/day3/ci/39111621696/baseline/runtime-baseline.json). Earlier failed runs remain historical, with their original conclusions preserved.

The accepted 186 risks have **not** been fixed by this closeout. The actual code fix is the deployment/runtime readiness race. Image/Kubernetes hardening and security remediation remain separate work; Day 4 is not started because the required program acknowledgement is not completed. The user requested help, and its LMS page link is needed. No personal attestation or signature is fabricated.
