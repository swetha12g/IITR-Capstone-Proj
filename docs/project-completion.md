# Remaining assignment execution — current state

Updated 22 October 2026. The user directed completing the study project first and deferring vulnerability remediation. [Deferred register](deferred-remediation.md) lists every critical/high issue alias; full safe JSON also retains lower severities. Findings do not halt the study profile. Missing executions and failed APIs are recorded honestly rather than labeled successful.

| Stage | Actual state | Remaining work |
|---|---|---|
| Days 1–4 | Prior source/build/hardening evidence retained; study-lab profile now continues with deferred risks | Keep strict historical verdict separate from the study verdict |
| Day 5 | Complete local six-stage execution passed; build/test + SAST/SCA/secrets/IaC/container/DAST receipts share run/commit/image identities; ZAP reached 121 URLs; cleanup verified | Validate/publish/run the new hosted workflow; fresh-directory reproduction still pending |
| Day 6 | Current normalization: 372 observations, 235 underlying issues; dashboard and JSON/CSV built; curated 21-case dataset has TP14/FP0/FN1/TN6 | Recompute after final reproduction; labels are post-hoc and not independently human reviewed |
| Day 7 | 60 current tests cover normalization, aggregate contracts, redaction, grounding and bounded patches; actual mock HTTP bodies exclude private fields; refusals make zero calls | Keep the proof hash synchronized with the final boundary code/prompt |
| Day 8 | OpenAI-only client implemented with explicit live mode, official endpoint, existing external credential, three-request/$1 upper bounds and no billing changes. Read-only model access returned 200 | All three bounded generation attempts returned HTTP429; no successful live triage or actual token usage/cost is claimed. No further automatic attempts or purchases |
| Day 9 | Three Codex-authored focused proposals each fail the selected Checkov control before, pass after, and pass real Ready/HTTP checks in isolated namespaces; all namespaces deleted | Create three independent draft PRs and record genuine review. Do not claim the unavailable external API generated the plans |
| Day 10 | Reproduction/bootstrap code authored; report dependencies isolated; PDF/report and defense preparation underway | Fresh clone run, rendered 12-page visual QA, final evidence/privacy audit and publication |

Latest complete local pipeline run: `20261022T145253045022Z`, 115.75 seconds after explicit reuse of the freshly verified build/test (144.17 seconds measured separately). Six scanner jobs + build/test + aggregate are authored in `.github/workflows/study-pipeline.yml`; actionlint passes. No hosted run for that new workflow is claimed yet.

The repeated upstream availability run had six DNS-dependent failures. The explicit `offline-local` profile excludes the entire independent internet-resource availability suite (nine tests), then passes 1,372 frontend, 417 server and 537 local API tests: **2,326 passed, seven upstream skips, zero failures**. This is different from the historical online profile; the failed run is retained. Application source and both dependency locks remain unchanged.

Three proposal verification records are in [proposals.json](../reports/sanitized/day9/proposals.json). These are focused examples against the legacy baseline manifest, not closure of the full risk register. Coding-assistant authorship is real; external API generation, independent approval and merges are not fabricated. New commits/pushes/PRs are to be performed only as part of completing the requested project delivery after the concrete local review.

No browser surface was available for the attempted dashboard UI check; data/formula tests and HTML generation passed. PDF rendering/visual verification uses local Poppler images. No cloud account, billing, host sysctl/module or unrelated application is changed by these stages.

Bootstrap verification passed, and the first generated PDF has exactly twelve pages. All twelve pages were rendered with Poppler and inspected together for clipping, overflow and page order. Fresh-clone execution and draft PR publication are the next delivery steps. The automatic workflow is now the study pipeline; the original strict baseline remains available for manual historical verification. No exact source-exception policy was widened.
