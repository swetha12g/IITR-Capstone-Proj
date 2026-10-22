# GitHub Actions study report

The aggregate job publishes one detailed Markdown poster to the workflow run's **Summary** using `GITHUB_STEP_SUMMARY`. It runs after aggregation with `if: always()`, including when a mandatory job or the critical gate fails. GitHub documents this mechanism in [Adding a job summary](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-job-summary).

The poster includes current hosted stage/severity counts, actual test totals, pipeline-contract counts, SBOM size, exact-image runtime and passive-crawl coverage, repair decisions, deferred work, assessment limitations, immutable document links and receipt hashes. Counts are cross-stage observations; the separately labeled pre-commit local deduplicated register is historical context. Missing evidence is unverified and stale run/commit receipts cannot produce a passing poster. Raw scanner matches and private logs are excluded.

Download `aggregate-study-evidence` from the run for the identical Markdown, seven sanitized receipts, aggregate JSON and checked-in twelve-page study PDF. The PDF/dashboard describe the verified pre-hosted local snapshot; the Summary describes fresh hosted execution. Artifact retention is fourteen days. The image-transfer artifact is separate and retained seven days.

## Publication verification — in progress

The critical fixes were committed as `8ac412e`. Local report/parser/AI-boundary checks pass 76 tests; actionlint passes. The parser was also checked against the actual prior frontend, server and API logs (1,372 / 422 / 538 passes; zero / two / four skips). Its failure controls cover critical findings, missing receipts, stale identities, mixed images and malformed/missing test totals. Hosted results and the downloaded poster hash will be recorded after the push and completed run.
