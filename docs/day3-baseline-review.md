# Day 3 baseline risk review — exact lab exceptions approved

Date: 18 October 2026, Asia/Kolkata. The designated project-owner reviewer explicitly accepted the current **186 exact lab-only exceptions** on this date. They are now active until **25 October 2026 at 00:00 IST**; verification is being rerun. This is acceptance of visible risk, not a finding fix.

The actual scans produced 221 distinct metadata fingerprints, of which **186 block**: 8 SAST high candidates, 42 distinct high/critical dependency findings, and 68 distinct history plus 68 distinct working-tree suspected-credential locations (69 raw rows in each secret scan). Trivy includes production **and development** dependencies: 74 raw rows represent 74 distinct dependency findings. Scanner matches are not automatically confirmed exploitability or real credentials.

## Coverage correction

The first 183-entry packet used Trivy's production-only default. That review request is superseded by this packet after explicitly enabling development dependency analysis. No additional package code is installed or executed. Existing finding identities remain present, with additional risks requiring their own owner acceptance.

## Proposed decision

Review [all 186 exact proposed entries](../reports/sanitized/day3/baseline-review-proposals.json). Accepting them would permit only those exact recorded identities/severities as visible baseline risk in this owned intentionally vulnerable lab, expiring **25 October 2026 at 00:00 IST**. New fingerprints, changed source/lock-file bytes at the same path/line, changed severity, expired/unreviewed exceptions or scanner/report failures remain blocking. Current-file exceptions are additionally bound to SHA-256; historical findings remain bound to their immutable Git commit. The earlier production-only 183-entry proposal is retained as a superseded historical packet. Any approval referring only to those 183 entries cannot approve additional findings. No wildcard, folder-wide suppression or finding deletion is proposed.

Every secret-match path is byte-identical to the public upstream pin, and every history match was introduced by the source-import commit; see [provenance proof](../reports/sanitized/day3/secret-provenance.json). This excludes newly added home/local credential material from these observed matches, but **does not prove that a published credential is safe**. No match values, raw lines, personal contact details or real credential validation are included. The upstream training Terraform files are scanned as source only and are not used to deploy the owned lab.

## SAST candidates

| Rule | Source path | Line | Severity |
|---|---|---|---|
| policies.semgrep.pf-sql-template-query | `app/juice-shop/data/static/codefixes/unionSqlInjectionChallenge_1.ts` | 6 | HIGH |
| policies.semgrep.pf-sql-template-query | `app/juice-shop/data/static/codefixes/unionSqlInjectionChallenge_3.ts` | 10 | HIGH |
| policies.semgrep.pf-sql-template-query | `app/juice-shop/data/static/codefixes/dbSchemaChallenge_3.ts` | 11 | HIGH |
| policies.semgrep.pf-sql-template-query | `app/juice-shop/routes/login.ts` | 34 | HIGH |
| policies.semgrep.pf-eval-input | `app/juice-shop/routes/userProfile.ts` | 65 | HIGH |
| policies.semgrep.pf-eval-input | `app/juice-shop/test/cypress/e2e/contact.spec.ts` | 267 | HIGH |
| policies.semgrep.pf-eval-input | `app/juice-shop/routes/captcha.ts` | 22 | HIGH |
| policies.semgrep.pf-sql-template-query | `app/juice-shop/routes/search.ts` | 23 | HIGH |

## Dependency candidates

| Advisory | Lock target | Component | Version | Severity |
|---|---|---|---|---|
| CVE-2026-26960 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2026-55849 | `package-lock.json` | @cyclonedx/cyclonedx-npm | 4.2.1 | HIGH |
| CVE-2026-27904 | `package-lock.json` | minimatch | 3.0.5 | HIGH |
| CVE-2026-106445 | `package-lock.json` | handlebars | 4.7.9 | CRITICAL |
| CVE-2026-23950 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2026-71851 | `package-lock.json` | crypto-js | 3.3.0 | CRITICAL |
| CVE-2026-48779 | `frontend/package-lock.json` | ws | 8.18.0 | HIGH |
| CVE-2026-59874 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2025-65945 | `package-lock.json` | jws | 0.2.6 | HIGH |
| CVE-2026-27903 | `package-lock.json` | minimatch | 3.0.5 | HIGH |
| NSWG-ECO-17 | `package-lock.json` | jsonwebtoken | 0.4.0 | HIGH |
| CVE-2026-102990 | `package-lock.json` | basic-ftp | 5.3.1 | HIGH |
| CVE-2021-23337 | `package-lock.json` | lodash | 2.4.2 | HIGH |
| CVE-2023-46233 | `package-lock.json` | crypto-js | 3.3.0 | CRITICAL |
| CVE-2022-24785 | `package-lock.json` | moment | 2.0.0 | HIGH |
| CVE-2015-9235 | `package-lock.json` | jsonwebtoken | 0.1.0 | CRITICAL |
| CVE-2026-73566 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2016-1000223 | `package-lock.json` | jws | 0.2.6 | HIGH |
| CVE-2026-26996 | `package-lock.json` | minimatch | 3.0.5 | HIGH |
| CVE-2026-93687 | `frontend/package-lock.json` | braces | 3.0.3 | HIGH |
| NSWG-ECO-428 | `package-lock.json` | base64url | 0.0.6 | HIGH |
| CVE-2022-23539 | `package-lock.json` | jsonwebtoken | 0.4.0 | HIGH |
| CVE-2026-59873 | `package-lock.json` | tar | 6.2.1 | CRITICAL |
| CVE-2026-29786 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2017-18214 | `package-lock.json` | moment | 2.0.0 | HIGH |
| CVE-2026-31802 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2026-71538 | `package-lock.json` | @cyclonedx/cyclonedx-npm | 4.2.1 | HIGH |
| CVE-2026-23745 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2026-101894 | `package-lock.json` | decompress | 4.2.1 | CRITICAL |
| CVE-2019-10744 | `package-lock.json` | lodash | 2.4.2 | CRITICAL |
| CVE-2018-16487 | `package-lock.json` | lodash | 2.4.2 | HIGH |
| CVE-2022-23539 | `package-lock.json` | jsonwebtoken | 0.1.0 | HIGH |
| CVE-2026-53486 | `package-lock.json` | decompress | 4.2.1 | CRITICAL |
| CVE-2026-24842 | `package-lock.json` | tar | 6.2.1 | HIGH |
| CVE-2026-93748 | `package-lock.json` | http-cache-semantics | 3.8.1 | HIGH |
| CVE-2015-9235 | `package-lock.json` | jsonwebtoken | 0.4.0 | CRITICAL |
| NSWG-ECO-17 | `package-lock.json` | jsonwebtoken | 0.1.0 | HIGH |
| CVE-2026-106446 | `package-lock.json` | handlebars | 4.7.9 | CRITICAL |
| CVE-2020-15084 | `package-lock.json` | express-jwt | 0.1.3 | HIGH |
| CVE-2022-25881 | `package-lock.json` | http-cache-semantics | 3.8.1 | HIGH |
| GHSA-5mrr-rgp6-x4gr | `package-lock.json` | marsdb | 0.6.11 | CRITICAL |
| CVE-2022-25887 | `package-lock.json` | sanitize-html | 1.4.2 | HIGH |

## Suspected-credential candidates, grouped for navigation

Exact line/commit fingerprints for both scans remain in the JSON proposal; grouping here does not broaden any exception.

| Rule | Source path | History matches | Working-tree matches |
|---|---|---|---|
| generic-api-key | `app/juice-shop/data/static/users.yml` | 2 | 2 |
| generic-api-key | `app/juice-shop/frontend/src/app/faucet/faucet.component.ts` | 1 | 1 |
| generic-api-key | `app/juice-shop/frontend/src/app/last-login-ip/last-login-ip.component.spec.ts` | 1 | 1 |
| generic-api-key | `app/juice-shop/frontend/src/app/oauth/oauth.component.spec.ts` | 2 | 2 |
| generic-api-key | `app/juice-shop/routes/login.ts` | 1 | 1 |
| generic-api-key | `app/juice-shop/test/api/2fa.test.ts` | 16 | 16 |
| generic-api-key | `app/juice-shop/test/api/basket.test.ts` | 2 | 2 |
| generic-api-key | `app/juice-shop/test/api/chat.test.ts` | 1 | 1 |
| generic-api-key | `app/juice-shop/test/api/checkKeys.test.ts` | 3 | 3 |
| generic-api-key | `app/juice-shop/test/api/data-export.test.ts` | 4 | 4 |
| generic-api-key | `app/juice-shop/test/api/erasure-request.test.ts` | 6 | 6 |
| generic-api-key | `app/juice-shop/test/api/feedback.test.ts` | 2 | 2 |
| generic-api-key | `app/juice-shop/test/api/login.test.ts` | 3 | 3 |
| generic-api-key | `app/juice-shop/test/api/product-review.test.ts` | 2 | 2 |
| generic-api-key | `app/juice-shop/test/api/user.test.ts` | 5 | 5 |
| generic-api-key | `app/juice-shop/test/cypress/e2e/login.spec.ts` | 1 | 1 |
| generic-api-key | `app/juice-shop/test/cypress/e2e/totpSetup.spec.ts` | 1 | 1 |
| jwt | `app/juice-shop/frontend/src/app/app.guard.spec.ts` | 1 | 1 |
| jwt | `app/juice-shop/frontend/src/app/last-login-ip/last-login-ip.component.spec.ts` | 1 | 1 |
| jwt | `app/juice-shop/test/api/user.test.ts` | 1 | 1 |
| jwt | `app/juice-shop/test/cypress/e2e/forgedJwt.spec.ts` | 3 | 3 |
| jwt | `app/juice-shop/test/server/currentUser.unit.test.ts` | 2 | 2 |
| jwt | `app/juice-shop/test/server/verify.unit.test.ts` | 4 | 4 |
| private-key | `app/juice-shop/infrastructure/terraform/networking.tf` | 1 | 1 |
| private-key | `app/juice-shop/lib/insecurity.ts` | 1 | 1 |
| private-key | `app/juice-shop/terraform/networking.tf` | 1 | 1 |

## Review status

The designated project-owner reviewer explicitly accepted the current 186-entry packet on 18 October 2026. [Approval receipt](../reports/sanitized/day3/owner-review.json) and [active policy](../policies/baseline-exceptions.json) record the exact scope and expiry. This user decision supersedes the pending state above; all entries remain visible as accepted baseline risk. The request to fix findings continues separately through measured remediation; no source or dependency fix is claimed by this approval. Day 4 and later stages remain unimplemented.
