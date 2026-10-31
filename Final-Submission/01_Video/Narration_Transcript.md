# Presentation transcript

Team names are spoken in the video and retained in `Narration_Transcript.txt`. This Markdown copy omits personal credits.

PipelineFortress presentation transcript

Female Indian English synthetic narration. Revised 31 October 2026.

00:00:00.000  PipelineFortress

Welcome to the Pipeline Fortress capstone presentation. Pipeline Fortress integrates security checks into software delivery for the OWASP Juice Shop training application. The recorded work covers six security stages and reduces the eleven baseline critical issues to zero in retained source and image scans. The selected application evidence records two thousand three hundred and thirty two passing tests. The published version one point zero point zero release includes all three focused infrastructure remediations.

This walkthrough explains how the pipeline links each security decision to a specific source revision and image. We will examine the implementation, the measured results, and the controls around AI assisted triage. The presentation uses recorded project evidence and a synthetic narrator. Detailed receipts and reproduction instructions accompany the submission.

Evidence: Project brief, sections 1, 6 and 8; docs/scope.md

00:00:53.239  Project team and presenters

The project team and presenters are:

[Presenter credit in the companion text transcript].

[Presenter credit in the companion text transcript].

[Presenter credit in the companion text transcript].

[Presenter credit in the companion text transcript].

[Presenter credit in the companion text transcript].

The next slides explain the engineering objective, the pipeline architecture, and the verification behind the release. We then examine security coverage, the AI data boundary, and the measured limits of the evaluation.

The source code, report, and evidence files support the technical discussion. Each reported result retains its own execution scope. The team credits identify the presenters without assigning individual implementation roles that the evidence does not establish. Let us begin with the delivery problem that the project addresses.

Evidence: Presenter credits supplied by the user. No individual implementation roles inferred.

00:01:43.976  Project objective and scope

The brief describes an engineering team that releases frequently and receives security feedback too late. Pipeline Fortress moves selected checks into the build and review process so developers can see findings before a release decision. The target is a pinned Juice Shop application in an owned training environment. No external systems or customer data are included.

The implementation includes static analysis, dependency analysis, secrets scanning, infrastructure checks, container scanning, and passive web scanning. The submission documents the implemented controls and their verification evidence. The scenario mentions catching eighty percent of vulnerabilities before merge. The available evaluation measures a small labeled fixture set. It cannot establish an eighty percent detection rate across the whole application or a production service.

Evidence: Project brief, sections 2, 5, 6 and 8; docs/scope.md

00:02:36.303  Pipeline architecture

The workflow starts with a pinned source checkout and the selected application build and test sequence. Source scanners inspect code, dependencies, history, and the working tree. A separate build produces the hardened image. Container analysis and software inventory operate on that exact image, and the staging job deploys the transferred artifact into an owned temporary Kubernetes cluster. Passive web scanning follows functional runtime checks.

Each job publishes a sanitized receipt with its run, revision, source identity, and relevant hashes. The aggregate job checks those identities before accepting the execution. This prevents a passing report from one revision being combined with an unrelated build or deployment. The workflow uses pinned action revisions and read only repository permissions. Cleanup removes the temporary staging resources belonging to that run.

Evidence: .github/workflows/study-pipeline.yml; scripts/aggregate-gate.py; scripts/image-transfer.py

00:03:30.645  Application verification

The release on main completes all eight workflow jobs successfully at the recorded release revision. The retained application evidence contains two thousand three hundred and thirty two passing tests and six skips. Nine tests that depend on external service availability are excluded from the offline profile. Server verification goes beyond a summary count. All four hundred and twenty four expected case and status identities match across forty one files, including five critical regression cases.

This matters because an earlier run omitted eleven server verdicts and the gate correctly rejected it. The accepted historical publication recorded eighty five safeguard contracts. Release preparation expanded verification to one hundred and twenty five local contracts, including the source gate checks. These counts describe distinct verification scopes. The release evidence and earlier scanner snapshots retain their own revision and execution dates.

Evidence: reports/sanitized/final-audit/publication-ci/verification.json; submission GitHub readback

00:04:28.247  Six security stages

Each scanner addresses a different part of the delivery path. Semgrep applies authored source rules. Trivy examines dependency and image inventories. Gitleaks checks both Git history and the current tree. Checkov evaluates infrastructure and Docker configuration, while ZAP performs a passive scan of the deployed application.

A completed scanner is not the same as a clean security result. The current study profile blocks critical findings, retains high and lower findings as deferred risk, and rejects missing, skipped, malformed, or inconsistent execution evidence. The retained local dashboard contains two hundred and fifty one observations representing one hundred and eighty underlying issues. The hosted publication contains two hundred and fifty seven cross stage observations. Those datasets come from different runs and counting scopes, so their totals must remain separate. Historical approvals also retain their original expiry dates.

Evidence: policies/; scripts/aggregate-gate.py; reports/sanitized/pipeline/aggregate.json

00:05:26.544  A restricted runtime

The hardened runtime uses a dedicated non root identity with user and group identifier sixty five thousand five hundred and thirty two. It drops capabilities, prevents privilege escalation, uses the runtime default seccomp profile, and makes the root filesystem read only. The application still needs writable locations for its database and selected training features. Explicit mounts provide those locations while protecting application code and immutable seed content.

Historical infrastructure checks improved from fifteen Kubernetes failures to one, and Dockerfile failures improved from two to zero. Those configuration improvements preceded the later dependency repair, so they are reported separately. Selected controls map to the documented CIS guidance, but a full benchmark certification is not claimed. Network policy enforcement remains unverified and must be addressed before a stronger deployment assurance claim.

Evidence: infra/docker/Dockerfile; infra/k8s-hardened/deployment.yaml; docs/day4-controls.md

00:06:23.955  Critical remediation and inventory

Later remediation addressed the eleven critical identities recorded in the baseline. The changes include dependency upgrades and replacements, together with repairs to affected application behavior. The tests now assert rejection of the relevant unsafe behavior rather than preserving exploit success. Retained source and rebuilt image scans report zero critical findings.

The local image still has five high observations, so the result does not establish that the application is free of vulnerabilities. Syft produced a schema validated Cyclone DX inventory with two thousand six hundred and fifty eight components for the recorded local image. The submission includes that existing hardened image as an archive and a derived inventory that omits private path metadata. Provenance links both to their original receipt. Local image identity and the separate hosted image identity remain explicitly distinguished.

Evidence: docs/critical-remediation.md; reports/sanitized/pipeline/container.json; SBOM provenance

00:07:18.752  Runtime coverage

The runtime evidence establishes that the selected application behavior survives the hardening and critical repairs. Seven functional checks pass against the owned deployment, and the deployed image agrees with the relevant build receipt. The passive ZAP run reaches one hundred and twenty one URLs and verifies seed routes including the home page, product search, languages, FTP, and metrics. Cleanup evidence confirms that the scanner and temporary resources were removed.

The scan uses a traditional unauthenticated crawler. It does not establish full single page application navigation, role coverage, business logic correctness, or the results of active attacks. Some intentionally vulnerable training behavior remains visible, including directory listing and error disclosure. Those observations stay in the deferred register. A successful runtime check proves a specific expectation and does not establish complete security.

Evidence: reports/sanitized/final-audit/publication-ci/verification.json; docs/runtime-baseline.md

00:08:14.963  Detection on labeled fixtures

The dashboard measures detection on twenty one deliberately selected unsafe and repaired fixture cases. Fifteen cases contain introduced issues. The scanners catch fourteen and miss one. Six negative cases are classified correctly, and this small set has no recorded false positives. Precision is therefore one hundred percent, recall is ninety three point three percent, and the F one score is ninety six point six percent.

The known miss is an unprotected synthetic export route that the six authored source patterns do not detect. Retaining that miss helps explain the rules coverage boundary. The labels were curated after the study work and have not received independent validation. These values describe scanner fixtures, not AI accuracy, and they do not estimate recall across all remaining application vulnerabilities. The scenario target is met only within this limited fixture set.

Evidence: metrics/labels.json; reports/sanitized/dashboard/index.json

00:09:10.599  Developer feedback timing

The dashboard separates observations from deduplicated underlying issues and exports the same data in HTML, JSON, and CSV formats. The primary local snapshot contains one hundred and eighty underlying issues, including ninety one high severity issues and zero critical issues. Timing is useful only when the build and setup scope is clear. The repaired fresh directory run took two hundred and seventy four point seven one pipeline seconds without build or test reuse.

Its first actionable receipt arrived at one hundred and sixty nine seconds. Bootstrap, downloads, and cluster creation add time outside that measurement. A different historical run reused a verified build and recorded ninety three point one nine seconds. Those timings are not interchangeable. Each is one observation, so the dashboard does not infer percentile latency, a service level commitment, or a measured production delivery improvement.

Evidence: reports/sanitized/dashboard/index.json; reproduction/critical-variant/run.json

00:10:07.410  AI input and output controls

The AI boundary constructs a new payload from an exact field allowlist. It does not forward raw scanner JSON and hope that masking removes every sensitive value. Generated aliases replace local identifiers, and advisory versions must come from the independently verified scanner catalog. The final serialized body receives additional checks. Captured mock requests demonstrate that private paths, source text, secret canaries, and scanner matches do not reach transport.

Invalid input refuses before a request is sent. Output validation checks identifiers, issue clusters, versions, operations, and required coverage. Invented advisories, unsupported versions, malformed fixes, and omissions fail validation. The model receives no shell or file write tools. These deterministic controls establish boundary behavior on the tested cases. They cannot prove how an unavailable live model would perform across a representative evaluation set.

Evidence: triage/redact.py; triage/validate.py; tests/redaction/; prompts/

00:11:08.992  Live AI evaluation remains open

The configured external AI triage path remains an open evaluation item. A read only model lookup succeeded, but all three bounded generation attempts returned HTTP four twenty nine. The records do not establish the underlying cause. No successful live model output or returned usage record is available. The project retains the failed attempts and the exhausted request cap.

A deterministic twenty finding mock batch passes through the same input boundary and output validation path. This verifies the integration contract and refusal controls on the tested cases. It cannot establish live model quality. Live precision, recall, hallucination frequency, and actual billed cost therefore remain unavailable. The coding assistant contribution to implementation and reporting is disclosed separately. The next evaluation step needs working, authorized model access and independently labeled cases.

Evidence: docs/ai-evaluation.md; reports/sanitized/day8/triage-live-error.json

00:12:06.139  Remediation and release promotion

The three remediation proposals modify the legacy baseline deployment manifest independently. The first disables service account token mounting because the application does not use the Kubernetes API. The second explicitly requires non root execution and the expected identity. The third adds a bounded HTTP liveness probe while retaining startup and readiness checks. For each proposal, the selected Checkov control fails before the change and passes afterward.

The deployment checks also reach readiness and pass selected HTTP expectations, with cleanup recorded. The coding assistant authored bounded local templates. The unavailable application API did not generate them. All three pull requests have now merged into the feature branch. Promotion then completed through develop and main, followed by the published version one point zero point zero release. Independent human review remains unverified, so first review correctness is still unmeasured.

Evidence: docs/release-promotion.md; reports/sanitized/release-v1.0.0/verification.json; docs/reviews.md

00:13:05.755  Reproduction and maturity

Reproduction starts from a separate full history checkout and uses project local pinned tools. The script rebuilds the application and image, executes the scanner stages, deploys an owned temporary kind cluster, runs passive DAST, checks mock triage, and regenerates the dashboard. Cleanup verifies removal of that run’s cluster. The submission preserves source history so that history scanning can execute without relying on an unavailable remote.

Earlier fresh directory checks used the same Docker host and standard caches. They are not fresh machine tests, and the submission does not claim a new full pipeline execution today. The maturity assessment uses selected OWASP SAMM practices as an organizing lens. Repeatable builds, security checks, and defect records demonstrate progress. Independent review, stronger deployment controls, and organizational evidence would be needed for a formal maturity assessment.

Evidence: scripts/reproduce.sh; docs/reproduction.md; docs/project-completion.md

00:14:02.254  Submission and next steps

The submission brings together the three required components: this fifteen minute project presentation, the editable deck and technical report, and the source code with related project files. The source snapshot now matches the published version one point zero point zero release. The package also includes full committed history, policy rules, a prompt library, the metrics dashboard, and verification receipts. The recorded local container and its inventory retain their own exact image provenance.

The demonstrated engineering results are six stage security coverage, identity checked evidence, zero critical findings in the retained repaired scans, and tested controls around AI input and output. The remaining assessment work is successful live model evaluation, independent validation of labels and reviews, and the student oral assessment. The package makes those boundaries visible for the reviewer. Thank you for reviewing Pipeline Fortress and the work of our project team.

Evidence: Final submission manifest; review matrix; project brief sections 6, 7 and 12
