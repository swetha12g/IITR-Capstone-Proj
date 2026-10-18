# PipelineFortress final report — working outline

Status: early outline, not a submission-ready report. Individual target: 12 pages. Evidence comes from [evidence-index.md](evidence-index.md); unresolved decisions are in [scope.md](scope.md).

1. **Problem and scope:** secure CI/CD with GenAI-assisted triage; individual Juice Shop lab; measured detection target and assessment constraints.
2. **Architecture and requirements:** six scan stages, aggregate gates, staging runtime, normalization, redaction boundary, local fix adapters, and human review. Architecture implementation is pending.
3. **Environment and reproducibility:** verified Linux environment, separate Node runtime, Python pins, real upstream fork, immutable source import, lockfiles, and command/evidence references.
4. **Runtime baseline:** source-built image deployed to an owned Ready kind lab; confirmed unauthenticated directory listing, exposed metrics and malformed-search error disclosure in [runtime-baseline.md](runtime-baseline.md). Scanner-only suspicions remain separate.
5. **Security scans and gates:** source/dependency/secret execution and Day 3 contracts/probes verified; 186 exact baseline risks accepted for the lab; IaC/image/DAST stages remain pending.
6. **Container/IaC hardening and SBOM:** exact image identity, functional checks, selected control mappings, before/after comparison, and package inventory. Pending.
7. **DAST and coverage:** observed routes, passive baseline findings, authentication/SPA limitations, and scanner connectivity. Pending.
8. **AI data flow and safeguards:** source-free payload contract, serialized mock-body assertions, refusal/no-call behavior, and injection handling before live API access. Pending.
9. **Triage and evaluation:** independent labels, duplicates, priorities, grounded references, real misses/errors, model/cost data, and first-pass validity. Pending.
10. **Three remediation PRs:** real findings, AI contribution, local patches, before/after tests, independent human reviews, and rollback. Pending reviewer assignment and implementation.
11. **Metrics and maturity:** recomputable denominators, feedback time, introduced/caught/missed counts, residual risks, and a named maturity framework. Pending.
12. **Ethics, disclosure, and references:** owned-lab boundary, confidential evidence handling, acknowledgement, actual GenAI assistance, limitations, and official sources.

## Verified Day 1 result

The pinned fork source was imported with matching contents and original MIT license. User-local Node 24.22.0/npm 11.19.1 and an isolated Python 3.10 environment are verified. Root/frontend dependency installation and the explicit production build passed. Selected frontend, server, and API suites produced 2,334 passed tests, 8 upstream skips, and zero failures. Dependency locks and imported tracked source remained unchanged after execution; see the evidence index for manifests and checksums.

Submission is 18 October 2026, with the project owner performing manual review. Independent GitHub approval/coordinator acceptance must be distinguished from author self-review. API provider/model and spending cap remain unconfirmed. The remaining pipeline and AI stages have not been implemented; this outline does not imply deadline readiness or production safety.

Do not fill pending sections with assumed outcomes. No application security or production-readiness claim follows from a successful baseline build alone.

## Verified Day 2 local result

Source-image build exited 0. The authored namespace, deployment and ClusterIP service passed Kubernetes server validation. The Kubernetes 1.37.0 node and Juice Shop pod are Ready; the running image config matches the local build. HTTP 200 and three runtime observations are confirmed using owned loopback requests. Hosted build/test/deployment/runtime and cleanup passed in [run 38957969793](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38957969793). Downloaded sanitized evidence and its artifact checksum were verified. The earlier failed deployment's exact cause remains unconfirmed because its private runner log was discarded; the successful run is not a historical root-cause claim. The remaining IaC/image/DAST scans, AI safeguards/evaluation, three reviewed remediation PRs and rendered 12-page report remain pending.

## Day 3 measured results and exact risk acceptance

Pinned Semgrep, Trivy and Gitleaks execute locally and in CI with private raw reports and sanitized metadata. Actual probes detect six unsafe source patterns, a reviewed dependency advisory and a generated nonfunctional canary; repaired fixtures pass and historical canary retention blocks. All 25 fail-closed gate contracts pass. Production and development graphs are included.

The application has **221 distinct visible findings**; the designated reviewer accepted **186 exact lab-only risks** until 25 October 2026 at 00:00 IST. The local and hosted source gates pass with zero blockers/errors. This is risk acceptance, not application/dependency remediation or production readiness.

[Run 39111621696](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696), code `d68686a`, passed source checks and the application baseline. A post-rollout pod-wait race was fixed; five regression cases and actual deployment/runtime verification pass, including a real terminating pod excluded while live readiness/image checks succeed. Six application stages exit 0, four runtime observations pass and cleanup succeeds. Downloaded ZIP hashes and metadata/log privacy were verified. The earlier failed-run conclusions remain retained, and the original Day 2 incident's cause remains unconfirmed.

Day 3 is complete for its defined scope. IaC/image/DAST, AI/evaluation, three reviewed remediation PRs and the rendered 12-page final report remain pending. The Day 4 program acknowledgement is not completed; assistance has been requested and its LMS page link is needed. No personal signature or attestation is fabricated.
