# 🛡️ PipelineFortress | Critical repair & CI report

> **✅ ZERO CRITICAL · STUDY GATE PASSED**

[This workflow run](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) · [Tested commit `1616f1428947`](https://github.com/swetha12g/IITR-Capstone-Proj/commit/1616f14289479ad7812a6501e10ac9baf62d4495) · [Full study PDF](https://github.com/swetha12g/IITR-Capstone-Proj/blob/1616f14289479ad7812a6501e10ac9baf62d4495/output/pdf/PipelineFortress_Study_Report.pdf)

| Critical observations | Mandatory receipts | Security stages | Operational errors |
| :---: | :---: | :---: | :---: |
| **0** | **7 / 7** | **6 required** | **0** |

**Scope:** educational study lab. Critical findings fail CI. High and lower findings remain visible and deferred; a passing study gate does not establish production readiness.

## 1 · Fresh hosted security results

| Stage | Job | Receipt | Critical | High | Medium | Low | Info | Unknown | Measured seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| build-test | success | complete | 0 | 0 | 0 | 0 | 0 | 0 | 518.46 |
| sast | success | complete | 0 | 8 | 3 | 0 | 0 | 0 | 6.84 |
| sca | success | complete | 0 | 10 | 9 | 4 | 0 | 0 | 8.89 |
| secrets | success | complete | 0 | 135 | 0 | 0 | 0 | 0 | 5.68 |
| iac | success | complete | 0 | 1 | 0 | 0 | 0 | 0 | 4.74 |
| container | success | complete | 0 | 5 | 26 | 10 | 0 | 0 | 34.75 |
| dast | success | complete | 0 | 0 | 9 | 21 | 16 | 0 | 55.57 |

| Current cross-stage totals | Critical | High | Medium | Low | Info | Unknown |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Observations | 0 | 159 | 47 | 35 | 16 | 0 |

**Counting rule:** these are scanner observations, including duplicates across source/image and history/tree scans. They are not globally deduplicated issues. Missing or mismatched evidence never proves zero. Durations are stage scopes, not workflow wall time.

## 2 · Application & pipeline verification

| Test suite | Passed | Failed | Skipped | Cancelled / todo |
| --- | ---: | ---: | ---: | ---: |
| test-frontend | 1372 | 0 | 0 | 0 / 0 |
| test-server | 422 | 0 | 2 | 0 / 0 |
| test-api | 538 | 0 | 4 | 0 / 0 |

Pipeline / AI boundary / report contracts: **76 tests**, 0 failures, 0 errors, 0 skipped.

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

[Detailed repair and negative-probe evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/1616f14289479ad7812a6501e10ac9baf62d4495/docs/critical-remediation.md) · [Local verification snapshot](https://github.com/swetha12g/IITR-Capstone-Proj/blob/1616f14289479ad7812a6501e10ac9baf62d4495/reports/sanitized/critical-remediation/verification.json)

The separate pre-commit local snapshot reported **180 unique issues: 0 critical, 91 high, 45 medium, 28 low, 16 informational**, with 2,332 application passes and six skips. Those historical unique totals are not substituted for this run’s observation counts. Its old/new immutable-image probes demonstrated rejection of unsigned JWTs and executable selectors. Signing keys rotate on process restart, requiring renewed sessions.

## 5 · Deferred work & assessment limits

- High/lower fixes: [deferred issue register](https://github.com/swetha12g/IITR-Capstone-Proj/blob/1616f14289479ad7812a6501e10ac9baf62d4495/docs/deferred-remediation.md).
- Successful live AI evaluation remains pending after three HTTP429 attempts; automatic request cap exhausted. This workflow makes no provider calls or purchases.
- Independent labels, human PR review and oral assessment remain outstanding. No reviewer approval or production certification is inferred.
- Secret scans retain intentional upstream training fixtures and history. Raw scanner matches, credentials, private logs and full SBOM contents are excluded from this report artifact.

[Project completion and remaining evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/1616f14289479ad7812a6501e10ac9baf62d4495/docs/project-completion.md) · [Evidence index](https://github.com/swetha12g/IITR-Capstone-Proj/blob/1616f14289479ad7812a6501e10ac9baf62d4495/docs/evidence-index.md) · [Dashboard snapshot source](https://github.com/swetha12g/IITR-Capstone-Proj/blob/1616f14289479ad7812a6501e10ac9baf62d4495/reports/sanitized/dashboard/index.html)

## 6 · Download & audit trail

Download **aggregate-study-evidence** from [this run’s artifacts](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944#artifacts): this exact Markdown poster, all seven sanitized stage receipts, aggregate JSON, and the twelve-page study PDF. The PDF and dashboard are the checked-in pre-hosted local snapshot; this Actions Summary records the fresh hosted execution.

<details>
<summary>Commit, image, source tree and receipt hashes</summary>

- Run: `39842575944`
- Commit: `1616f14289479ad7812a6501e10ac9baf62d4495`
- Source tree: `2cb817a0451c5c843b987c03b73828c89b32c93fbb2f4436b0e0b19ea0798174`
- Image config: `sha256:a6c68295948a3e8275b517244e4acab55c52820884847e776b63200dff1feb5d`

| Stage receipt | SHA-256 |
| --- | --- |
| build-test | `6dd678984eceb5311404236b510f74c7ecd260cd9871c849edd1d2831fb0cb22` |
| container | `44e2506e53921ab456425c15c3ff6a1e07a29a962f2c9d7e4076783032567866` |
| dast | `30b0e670478cecb4a2d1d9022514ed14bf0e3232ac1323fa2b34d1bfd381afc2` |
| iac | `aa6af95c7a2af3d2a050eeb3d9806e472aaaac8435f9d10adb93ad51ae740ad7` |
| sast | `4b7ed5b7c460f452505e3573cf5325b5d4e51da5777cfc46b25de256778f89cc` |
| sca | `a7d25c47d91052633b9f690a8ca2d296977126fd8179f3ecce212d703fdcd4d1` |
| secrets | `182eb48014354ff3ebc9fe82fe0034f4c24f80e059d0dbf971c79f5ee7e3988c` |

</details>

