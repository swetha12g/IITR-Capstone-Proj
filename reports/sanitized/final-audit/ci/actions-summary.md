# 🛡️ PipelineFortress | Critical repair & CI report

> **✅ ZERO CRITICAL · STUDY GATE PASSED**

[This workflow run](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39850270120) · [Tested commit `89d5db70dc2d`](https://github.com/swetha12g/IITR-Capstone-Proj/commit/89d5db70dc2d19fa5efce81a2439228518f3e6d7) · [Full study PDF](https://github.com/swetha12g/IITR-Capstone-Proj/blob/89d5db70dc2d19fa5efce81a2439228518f3e6d7/output/pdf/PipelineFortress_Study_Report.pdf)

| Critical observations | Mandatory receipts | Security stages | Operational errors |
| :---: | :---: | :---: | :---: |
| **0** | **7 / 7** | **6 required** | **0** |

**Scope:** educational study lab. Critical findings fail CI. High and lower findings remain visible and deferred; a passing study gate does not establish production readiness.

## 1 · Fresh hosted security results

| Stage | Job | Receipt | Critical | High | Medium | Low | Info | Unknown | Measured seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| build-test | success | complete | 0 | 0 | 0 | 0 | 0 | 0 | 295.35 |
| sast | success | complete | 0 | 8 | 3 | 0 | 0 | 0 | 7.35 |
| sca | success | complete | 0 | 10 | 9 | 4 | 0 | 0 | 13.80 |
| secrets | success | complete | 0 | 135 | 0 | 0 | 0 | 0 | 6.82 |
| iac | success | complete | 0 | 1 | 0 | 0 | 0 | 0 | 4.04 |
| container | success | complete | 0 | 5 | 26 | 10 | 0 | 0 | 33.75 |
| dast | success | complete | 0 | 0 | 10 | 21 | 16 | 0 | 60.34 |

| Current cross-stage totals | Critical | High | Medium | Low | Info | Unknown |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Observations | 0 | 159 | 48 | 35 | 16 | 0 |

**Counting rule:** these are scanner observations, including duplicates across source/image and history/tree scans. They are not globally deduplicated issues. Missing or mismatched evidence never proves zero. Durations are stage scopes, not workflow wall time.

## 2 · Application & pipeline verification

| Test suite | Passed | Failed | Skipped | Cancelled / todo |
| --- | ---: | ---: | ---: | ---: |
| test-frontend | 1372 | 0 | 0 | 0 / 0 |
| test-server | 395 | 0 | 2 | 0 / 0 |
| test-api | 538 | 0 | 4 | 0 / 0 |

Pipeline / AI boundary / report contracts: **79 tests**, 0 failures, 0 errors, 0 skipped.

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

[Detailed repair and negative-probe evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/89d5db70dc2d19fa5efce81a2439228518f3e6d7/docs/critical-remediation.md) · [Local verification snapshot](https://github.com/swetha12g/IITR-Capstone-Proj/blob/89d5db70dc2d19fa5efce81a2439228518f3e6d7/reports/sanitized/critical-remediation/verification.json)

The separate pre-commit local snapshot reported **180 unique issues: 0 critical, 91 high, 45 medium, 28 low, 16 informational**, with 2,332 application passes and six skips. Those historical unique totals are not substituted for this run’s observation counts. Its old/new immutable-image probes demonstrated rejection of unsigned JWTs and executable selectors. Signing keys rotate on process restart, requiring renewed sessions.

## 5 · Deferred work & assessment limits

- High/lower fixes: [deferred issue register](https://github.com/swetha12g/IITR-Capstone-Proj/blob/89d5db70dc2d19fa5efce81a2439228518f3e6d7/docs/deferred-remediation.md).
- Successful live AI evaluation remains pending after three HTTP429 attempts; automatic request cap exhausted. This workflow makes no provider calls or purchases.
- Independent labels, human PR review and oral assessment remain outstanding. No reviewer approval or production certification is inferred.
- Secret scans retain intentional upstream training fixtures and history. Raw scanner matches, credentials, private logs and full SBOM contents are excluded from this report artifact.

[Project completion and remaining evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/89d5db70dc2d19fa5efce81a2439228518f3e6d7/docs/project-completion.md) · [Evidence index](https://github.com/swetha12g/IITR-Capstone-Proj/blob/89d5db70dc2d19fa5efce81a2439228518f3e6d7/docs/evidence-index.md) · [Dashboard snapshot source](https://github.com/swetha12g/IITR-Capstone-Proj/blob/89d5db70dc2d19fa5efce81a2439228518f3e6d7/reports/sanitized/dashboard/index.html)

## 6 · Download & audit trail

Download **aggregate-study-evidence** from [this run’s artifacts](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39850270120#artifacts): this exact Markdown poster, all seven sanitized stage receipts, aggregate JSON, the twelve-page study PDF, and the dashboard HTML/JSON/CSV. The PDF and dashboard are checked-in evidence snapshots with their own run scopes; this Actions Summary records the fresh hosted execution.

<details>
<summary>Commit, image, source tree and receipt hashes</summary>

- Run: `39850270120`
- Commit: `89d5db70dc2d19fa5efce81a2439228518f3e6d7`
- Source tree: `0cadfc8f290900fe9c307f16acddfe17845266ddf493283b5624bdc3932ce832`
- Image config: `sha256:9fa46bc3e7dcbe7c322ac29e33862b7a729f4887a62c387c24ae4e8eb4adb1d0`

| Stage receipt | SHA-256 |
| --- | --- |
| build-test | `fc35e067b5f67c3f658624fee13857df5ce949dac0e46842e0a33e362aee4066` |
| container | `53e9a8dcfc38bfac1e0df43204fa3cd258c39885884bc867e34ab784163e6183` |
| dast | `d2417ab77541d52b5faa5d35dba145d5277d4dd851e91fb5f23e868f20ef30b7` |
| iac | `a02258a374b8e4c4d28693e360760291cdc6e70cad6bbfd0885d58a2a4f6f211` |
| sast | `00e17bbf020da1faa35ba1d6f02d2db02867707b3f82764590658fdc2d283863` |
| sca | `8cb7d747ce2830505608d5eabbeeb69a75da42eaf7a81719b7a55d9cec108aea` |
| secrets | `ab6ec0274ccc8c3f188e05cc4fcd0d21070a2093383154744d75a2661f108698` |

</details>

