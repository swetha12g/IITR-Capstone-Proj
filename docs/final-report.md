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

Pinned Semgrep, Trivy and Gitleaks execute locally with private raw reports and sanitized metadata. Six source rules, a verified dependency advisory and a generated nonfunctional token-shaped canary were detected by actual scanners; clean fixtures passed and historical canary retention was correctly blocking. All 25 gate contracts passed, including operational errors, exact expiring approvals, source/lock-content binding and metadata-only publication. The application has 221 distinct findings and 186 blockers before review. Hosted scanner/contract/probe evidence is verified; the designated reviewer has now explicitly accepted those 186 exact lab-only risks until 25 October at 00:00 IST. The fresh local source gate passes with zero blockers/errors; hosted source verification also passed in run `39110505372`; the parallel baseline hit a post-rollout pod-wait race; a narrow correction passed local redeploy/runtime and awaits hosted confirmation. This is risk acceptance, not remediation; there is no six-stage gate, measured detection-rate or production-safety claim.
