# 🛡️ PipelineFortress | Critical repair & CI report

> **✅ ZERO CRITICAL · STUDY GATE PASSED**

[This workflow run](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39912532895) · [Tested commit `42afe37ed4dd`](https://github.com/swetha12g/IITR-Capstone-Proj/commit/42afe37ed4dd44f5760c616ee42ff7854ce32940) · [Full study PDF](https://github.com/swetha12g/IITR-Capstone-Proj/blob/42afe37ed4dd44f5760c616ee42ff7854ce32940/output/pdf/PipelineFortress_Study_Report.pdf)

| Critical observations | Mandatory receipts | Security stages | Operational errors |
| :---: | :---: | :---: | :---: |
| **0** | **7 / 7** | **6 required** | **0** |

**Scope:** educational study lab. Critical findings fail CI. High and lower findings remain visible and deferred; a passing study gate does not establish production readiness.

## 1 · Fresh hosted security results

| Stage | Job | Receipt | Critical | High | Medium | Low | Info | Unknown | Measured seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| build-test | success | complete | 0 | 0 | 0 | 0 | 0 | 0 | 320.77 |
| sast | success | complete | 0 | 8 | 3 | 0 | 0 | 0 | 7.35 |
| sca | success | complete | 0 | 10 | 9 | 4 | 0 | 0 | 7.84 |
| secrets | success | complete | 0 | 135 | 0 | 0 | 0 | 0 | 7.65 |
| iac | success | complete | 0 | 1 | 0 | 0 | 0 | 0 | 4.29 |
| container | success | complete | 0 | 5 | 26 | 10 | 0 | 0 | 33.08 |
| dast | success | complete | 0 | 0 | 9 | 21 | 16 | 0 | 56.92 |

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

[Detailed repair and negative-probe evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/42afe37ed4dd44f5760c616ee42ff7854ce32940/docs/critical-remediation.md) · [Local verification snapshot](https://github.com/swetha12g/IITR-Capstone-Proj/blob/42afe37ed4dd44f5760c616ee42ff7854ce32940/reports/sanitized/critical-remediation/verification.json)

The separate pre-commit local snapshot reported **180 unique issues: 0 critical, 91 high, 45 medium, 28 low, 16 informational**, with 2,332 application passes and six skips. Those historical unique totals are not substituted for this run’s observation counts. Its old/new immutable-image probes demonstrated rejection of unsigned JWTs and executable selectors. Signing keys rotate on process restart, requiring renewed sessions.

## 5 · Deferred work & assessment limits

- High/lower fixes: [deferred issue register](https://github.com/swetha12g/IITR-Capstone-Proj/blob/42afe37ed4dd44f5760c616ee42ff7854ce32940/docs/deferred-remediation.md).
- Successful live AI evaluation remains pending after three HTTP429 attempts; automatic request cap exhausted. This workflow makes no provider calls or purchases.
- Independent labels, human PR review and oral assessment remain outstanding. No reviewer approval or production certification is inferred.
- Secret scans retain intentional upstream training fixtures and history. Raw scanner matches, credentials, private logs and full SBOM contents are excluded from this report artifact.

[Project completion and remaining evidence](https://github.com/swetha12g/IITR-Capstone-Proj/blob/42afe37ed4dd44f5760c616ee42ff7854ce32940/docs/project-completion.md) · [Evidence index](https://github.com/swetha12g/IITR-Capstone-Proj/blob/42afe37ed4dd44f5760c616ee42ff7854ce32940/docs/evidence-index.md) · [Dashboard snapshot source](https://github.com/swetha12g/IITR-Capstone-Proj/blob/42afe37ed4dd44f5760c616ee42ff7854ce32940/reports/sanitized/dashboard/index.html)

## 6 · Download & audit trail

Download **aggregate-study-evidence** from [this run’s artifacts](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39912532895#artifacts): this exact Markdown poster, all seven sanitized stage receipts, aggregate JSON, the twelve-page study PDF, and the dashboard HTML/JSON/CSV. The PDF and dashboard are checked-in evidence snapshots with their own run scopes; this Actions Summary records the fresh hosted execution.

<details>
<summary>Commit, image, source tree and receipt hashes</summary>

- Run: `39912532895`
- Commit: `42afe37ed4dd44f5760c616ee42ff7854ce32940`
- Source tree: `8a558f581516c2a445c3e8f2d8fff201923c3e1acba77a7d6509f23385924be0`
- Image config: `sha256:0e87d1f74b1ec83d4f5b1cb45248ae562786b324c28f756e256e9e1bc956394b`

| Stage receipt | SHA-256 |
| --- | --- |
| build-test | `0f28376fadce6b1d26405ff88376781bf70648046120b86cb9d696b500697b67` |
| container | `1cef278414f6af2ecd5b18b073bf2b501de9c9fb36002929a393db4cd73e8684` |
| dast | `08317e1a80497141bafe049bbdbb1cb9d3709530d0c8be5dae6b10523b6bb6d0` |
| iac | `4a62b70b1c267348659383923e083c0c4172062ad7517621d6c93f40c62fb4ac` |
| sast | `87d9b1c5524b3cc35530bd7bafe61fa59c47595a480c9b37d84750b2d3e6f894` |
| sca | `2ed0d9978657b74239c52eb43463a1a9ce7971c180aa17e8a11530a46776bf91` |
| secrets | `bef94c63548fd32735c408e80284ff3b02bca938624b4b281aa989dc1ea6cd32` |

</details>

