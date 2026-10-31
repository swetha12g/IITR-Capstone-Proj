# Critical dependency remediation

Final documentation/privacy review: 23 October 2026 IST; scanner/runtime execution timestamps remain recorded in UTC in the receipts.

The user requested fixing the previously deferred 11 critical underlying issues and reaching zero critical findings. This supersedes critical-risk deferral; high and lower severities remain deferred. No external AI request, purchase or billing change is part of this work.

## Verified changes

- Upgrade both old JWT dependency paths to modern verification, restrict authentication to RS256, and replace the public training signing key with a process-local generated 2048-bit key. Sessions do not survive a backend restart.
- Replace unpatched MarsDB with the maintained NeDB fork behind the existing collection interface. Reject executable selectors recursively and use typed review/order queries. Preserve insertion order and legacy update result shapes.
- Replace the downloader that introduced unpatched archive extraction with a bounded HTTP-only download operation that returns bytes without extraction.
- Upgrade the sanitizer to remove its old Lodash dependency; upgrade transitive Handlebars, CryptoJS and tar to patched versions through recorded npm overrides.
- Make critical findings fail the pipeline aggregate while retaining lower severities. Bind new scanner receipts to the project tree, including uncommitted implementation changes.

The seven affected dependency families include two old JWT versions. The original 11 issue identities are preserved in [the before receipt](../reports/sanitized/critical-remediation/before.json). Package names/versions were resolved by npm, with integrity hashes retained in the updated lock; no finding suppression or severity downgrade is applied.

## Verified outcome

**Critical underlying issues: 11 → 0.** Fresh source scanning includes development dependencies; exact-image scanning covers installed OS and application packages. Both use Trivy 0.76.0 without vulnerability ignore entries or severity downgrades. [Verification receipt](../reports/sanitized/critical-remediation/verification.json) binds raw report hashes, the updated lock, exact image and locally modified project tree.

| Dependency family | Before | Remediation |
|---|---|---|
| JWT | 0.1.0 and 0.4.0 | jsonwebtoken 9.0.3 and express-jwt 8.5.1; RS256 allowlist and fresh 2048-bit signing key |
| MarsDB | 0.6.11; no upstream patch | Replace with @seald-io/nedb 4.1.2; reject executable selectors; use typed review/order lookups |
| Archive extraction | decompress 4.2.1; no upstream patch | Remove its downloader dependency; make-fetch-happen 16.0.1 downloads bytes with a time/size bound and no extraction |
| Handlebars | 4.7.9 | 4.7.10 |
| CryptoJS | 3.3.0 | 4.2.0 |
| Lodash | 2.4.2 under the old sanitizer | sanitize-html 2.18.1 removes the old dependency; remaining Lodash is 4.18.1 |
| tar | 6.2.1 | 7.5.19 |

All six scanner stages and build/test passed in run `20261022T181348556832Z`: zero critical observations, zero security blockers and zero operational errors. The scan/runtime sequence took 93.19 seconds after explicit reuse of the fresh application/image checks. The full six-step application sequence took 143.51 seconds separately; setup and cluster creation are additional. Every stage binds the same project-tree hash. That local measurement used uncommitted changes on base `895ee08`; subsequent commits and fresh hosted verification are recorded below.

The selected application suites have **2,332 passed, six upstream skips and zero failures**: frontend 1,372; server 422; local API 538. Nine external availability tests remain explicitly excluded. Sixty-four pipeline/safeguard contracts, 25 source-gate contracts, five new critical regression tests, lint and snippet consistency checks pass. Server unit coverage regenerated successfully (41.85% lines; not a whole-application coverage claim).

Seven Docker checks, seven temporary Kubernetes checks and seven checks on the existing owned study deployment pass against image configuration `sha256:483df66c5bdfb2d47a740243a6db215e6abe43637a3bf23863ebc857997a59d0`. The existing owned workload was updated to that image. The temporary cluster and probe containers were removed. No host kernel settings or unrelated workloads changed; complete recovery of historical original-cluster system pods is not claimed.

[Old/new immutable-image probes](../reports/sanitized/critical-remediation/negative-probes.json) show that the old image accepts an unsigned JWT and executes a harmless in-memory query marker; the current exact image rejects both. [Gate control](../reports/sanitized/critical-remediation/gate-probe.json) proves CLI exit0 for zero critical and exit1 when a synthetic critical count is introduced. It does not modify actual scanner evidence.

Current normalization contains 251 observations / 180 underlying issues: **0 critical, 91 high, 45 medium, 28 low and 16 informational**. High and lower findings remain deferred. The schema-validated current SBOM has 2,658 components. The historical Day 4 image comparison and its 2,748-component inventory remain explicitly historical.

The dashboard and twelve-page report now reflect the current results; all report pages were rendered and visually checked. The pre-remediation PDF is retained under output history. Original import/CI receipts, earlier failure records and three infrastructure PRs remain historical evidence.

## Compatibility and remaining scope

Tests now expect rejection of forged JWTs, executable review/order queries and the old sanitizer bypass. Those training exploits are no longer solvable in this variant. Signing keys are process-local, so a backend restart requires signing in again. The root dependency lock is updated; the frontend lock, original license and exact historical source-approval file are unchanged. No finding suppressions or new exception entries are used.

No full legacy Cypress challenge-suite pass is claimed; no Cypress binary is installed. Independent review remains pending; subsequent hosted CI publication is recorded below. Successful live AI, independent label/PR review and oral assessment remain separate project requirements. No additional provider request, purchase, billing change, commit or push occurred during the local repair phase.

## Primary references

- [MarsDB advisory: no patched release](https://github.com/advisories/GHSA-5mrr-rgp6-x4gr).
- [Unmaintained decompressor and maintained alternatives](https://github.com/advisories/GHSA-hrh2-vp3x-79xf).
- [Handlebars 4.7.10 security release](https://github.com/handlebars-lang/handlebars.js/releases/tag/v4.7.10).
- [tar security advisory and patched release](https://github.com/advisories/GHSA-23hp-3jrh-7fpw).
- [Maintained NeDB API](https://github.com/seald/nedb), [HTTP download API](https://github.com/npm/make-fetch-happen), [JWT verification API](https://github.com/auth0/node-jsonwebtoken).

Final privacy/link review: changed/new files and extracted PDF text were scanned. Gitleaks reports ten unchanged upstream test-fixture lines, each verified byte-for-byte against the base commit; no new matched credential content was introduced. No new ignore entries were added and no zero-finding secrets-scan claim is made. [Review receipt](../reports/sanitized/critical-remediation/publication-review.json). Current evidence hashes and local file links validate.

## Subsequent hosted publication — 23 October 2026 IST

The user separately authorized commits, push and hosted verification. Repair commit `8ac412e` and report/workflow commit `1616f14` are pushed. [Run 39842575944](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) passed all eight jobs on `1616f14`, with zero critical findings, 2,332 application passes / six skips, 76 contracts, validated SBOM and all seven runtime checks. The Summary and ten-file report packet are published; official archive digest, gate recomputation, identity/image linkage and identical poster bytes are verified. [Hosted verification](../reports/sanitized/critical-remediation/ci/verification.json). The original local receipt and PDF retain their historical measurement scope. [Actions poster design and verification](actions-summary.md).
