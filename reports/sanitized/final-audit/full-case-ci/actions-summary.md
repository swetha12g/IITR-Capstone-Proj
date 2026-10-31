# 🛡️ PipelineFortress | Critical repair & CI report

> **✅ ZERO CRITICAL · STUDY GATE PASSED**

[This workflow run](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39910883934) · [Tested commit `06c8e1d4e7e3`](https://github.com/swetha12g/IITR-Capstone-Proj/commit/06c8e1d4e7e36041d80071aa1a1d506e50a2d633) · [Full study PDF](https://github.com/swetha12g/IITR-Capstone-Proj/blob/06c8e1d4e7e36041d80071aa1a1d506e50a2d633/output/pdf/PipelineFortress_Study_Report.pdf)

| Critical observations | Mandatory receipts | Security stages | Operational errors |
| :---: | :---: | :---: | :---: |
| **0** | **7 / 7** | **6 required** | **0** |

**Scope:** educational study lab. Critical findings fail CI. High and lower findings remain visible and deferred; a passing study gate does not establish production readiness.

## 1 · Fresh hosted security results

| Stage | Job | Receipt | Critical | High | Medium | Low | Info | Unknown | Measured seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| build-test | success | complete | 0 | 0 | 0 | 0 | 0 | 0 | 331.45 |
| sast | success | complete | 0 | 8 | 3 | 0 | 0 | 0 | 4.83 |
| sca | success | complete | 0 | 10 | 9 | 4 | 0 | 0 | 8.55 |
| secrets | success | complete | 0 | 135 | 0 | 0 | 0 | 0 | 8.08 |
| iac | success | complete | 0 | 1 | 0 | 0 | 0 | 0 | 4.95 |
| container | success | complete | 0 | 5 | 26 | 10 | 0 | 0 | 34.95 |
| dast | success | complete | 0 | 0 | 10 | 21 | 16 | 0 | 59.65 |

| Current cross-stage totals | Critical | High | Medium | Low | Info | Unknown |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Observations | 0 | 159 | 48 | 35 | 16 | 0 |

**Counting rule:** these are scanner observations, including duplicates across source/image and history/tree scans. They are not globally deduplicated issues. Missing or mismatched evidence never proves zero. Durations are stage scopes, not workflow wall time.

## 2 · Application & pipeline verification

| Test suite | Passed | Failed | Skipped | Cancelled / todo |
| --- | ---: | ---: | ---: | ---: |
| test-frontend | 1372 | 0 | 0 | 0 / 0 |
| test-server | 422 | 0 | 2 | 0 / 0 |
| test-api | 538 | 0 | 4 | 0 / 0 |

Server case inventory: **424 / 424** cases; 0 missing; 5 critical-remediation regressions. Case identities are hashed; raw names and JUnit paths remain private.

Pipeline / AI boundary / report contracts: **85 tests**, 0 failures, 0 errors, 0 skipped.

A successful build-test job includes pinned installs, frontend/backend build, selected local application tests, lint and snippet consistency. The independent internet-resource availability suite is excluded; other skips are shown above. Legacy Cypress challenge E2E coverage is not claimed.

## 3 · Exact-image inventory, runtime & passive DAST

| Evidence | Result |
| --- | --- |
| CycloneDX SBOM schema | verified |
| Image components | 2658 |
| Kubernetes HTTP checks | 7 / 7 |
| Passive DAST URLs reached | 121 |
| Required seeded routes | verified |
| Scanner container cleanup | verified |

Runtime checks cover the owned ephemeral Kubernetes deployment. Controls include non-root execution, a read-only root filesystem, dropped capabilities, no privilege escalation and absent service-account token. The DAST job also proves bad/fixed passive-header fixtures and removes its owned cluster in an always-run cleanup step; inspect its job result for cleanup failures. Passive unauthenticated crawling does not cover every route or authenticated attack.

## 4 · Critical repair record

The pre-repair local register held **11 unique critical issues** (22 source/image observations). The dependency families below were repaired and regression-tested before publication; the live table above is the authoritative result for this commit.

| Family | Repair |
| --- | --- |
| JWT / express-jwt | jsonwebtoken 9.0.3, express-jwt 8.5.1; explicit RS256 and generated 2048-bit keys |
| MarsDB | Replaced with @seald-io/nedb 4.1.2; executable selectors rejected, typed queries |
| decompress / download | Removed extraction dependency; bounded streamed HTTP download |
| Handlebars | 4.7.10 override |
| crypto-js | 4.2.0 override |
| Lodash / sanitizer | sanitize-html 2.18.1; vulnerable Lodash 2.x path removed |
| tar | 7.5.19 override |

[Detailed repair and negative-probe evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/06c8e1d4e7e36041d80071aa1a1d506e50a2d633/docs/critical-remediation.md) · [Local verification snapshot](https://github.com/swetha12g/IITR-Capstone-Proj/blob/06c8e1d4e7e36041d80071aa1a1d506e50a2d633/reports/sanitized/critical-remediation/verification.json)

The separate pre-commit local snapshot reported **180 unique issues: 0 critical, 91 high, 45 medium, 28 low, 16 informational**, with 2,332 application passes and six skips. Those historical unique totals are not substituted for this run’s observation counts. Its old/new immutable-image probes demonstrated rejection of unsigned JWTs and executable selectors. Signing keys rotate on process restart, requiring renewed sessions.

## 5 · Deferred work & assessment limits

- High/lower fixes: [deferred issue register](https://github.com/swetha12g/IITR-Capstone-Proj/blob/06c8e1d4e7e36041d80071aa1a1d506e50a2d633/docs/deferred-remediation.md).
- Successful live AI evaluation remains pending after three HTTP429 attempts; automatic request cap exhausted. This workflow makes no provider calls or purchases.
- Independent labels, human PR review and oral assessment remain outstanding. No reviewer approval or production certification is inferred.
- Secret scans retain intentional upstream training fixtures and history. Raw scanner matches, credentials, private logs and full SBOM contents are excluded from this report artifact.

[Project completion and remaining evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/06c8e1d4e7e36041d80071aa1a1d506e50a2d633/docs/project-completion.md) · [Evidence index](https://github.com/swetha12g/IITR-Capstone-Proj/blob/06c8e1d4e7e36041d80071aa1a1d506e50a2d633/docs/evidence-index.md) · [Dashboard snapshot source](https://github.com/swetha12g/IITR-Capstone-Proj/blob/06c8e1d4e7e36041d80071aa1a1d506e50a2d633/reports/sanitized/dashboard/index.html)

## 6 · Download & audit trail

Download **aggregate-study-evidence** from [this run’s artifacts](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39910883934#artifacts): this exact Markdown poster, all seven sanitized stage receipts, aggregate JSON, the twelve-page study PDF, and the dashboard HTML/JSON/CSV. The PDF and dashboard are checked-in evidence snapshots with their own run scopes; this Actions Summary records the fresh hosted execution.

<details>
<summary>Commit, image, source tree and receipt hashes</summary>

- Run: `39910883934`
- Commit: `06c8e1d4e7e36041d80071aa1a1d506e50a2d633`
- Source tree: `8a558f581516c2a445c3e8f2d8fff201923c3e1acba77a7d6509f23385924be0`
- Image config: `sha256:f6009212c760b51c64523806973c7f31b9f1538975025d94b67e0e8098abf247`

| Stage receipt | SHA-256 |
| --- | --- |
| build-test | `ac46f5d4452fdd7dea189d458533efe38749984ff149987cdb9b0d547c84dcd3` |
| container | `241e14b40a268c5afd2c9817db0e903d43a19f76f02f92eacc344cf71be37734` |
| dast | `934bdffdb8d4b0ccdc0ffa8a3b34078e7a4e47a9453a5609a58aea2e39284ea5` |
| iac | `7e833386ead8ddbaa8af4979a9f6ee301b0429d65e413fa4028117ed3f36f66a` |
| sast | `e3f147f86786d8c1eee83c03a83e42820f9e2f4248dd71e64fe7eb3e4b77aa47` |
| sca | `c2031718c5aa4853ec8e96959028fd77146b9b293cb5f1dc411824d985edce03` |
| secrets | `423a3487e28f70cc0c277e3fa36fae36622c515401979b2e8700e0f9ccf4cb77` |

</details>

