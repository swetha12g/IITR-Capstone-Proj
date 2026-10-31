# PipelineFortress operating scope

Updated: 22 October 2026; earlier planning dates remain historical.

| Decision | Recorded choice | Evidence / remaining dependency |
|---|---|---|
| Execution mode | Individual | Confirmed by the user on 17 October |
| Target | OWASP Juice Shop in the owned local lab | No external targets are in scope |
| Source acquisition | Separate GitHub fork plus a provenance-preserving import | Fork verified as a child of the official upstream; see [upstream-provenance.md](upstream-provenance.md) |
| Application pin | v20.3.0, commit `f189f521266f42c6bd05884468292000cee852ed` | Verified tag and fetched commit |
| Security coverage | SAST, SCA, secrets, IaC, container, DAST | All six remain required |
| Remediation deliverable | Three independent AI-assisted PRs | Actual findings, before/after evidence, and real human review required |
| Report | 12 pages | Default individual scope from the execution guide |
| Submission date | 18 October 2026 | Confirmed by the user on 17 October; exact cutoff time not supplied |
| Manual reviewer | Project owner | Confirmed by the user; retain genuine manual review notes for each proposed change |
| Independent PR approval / coordinator role | Pending where required | An author cannot approve their own GitHub PR; manual self-review is distinct from an independent approving review. Confirm acceptable individual-assessment evidence with the coordinator |
| API provider/model and spend cap | OpenAI GPT-6 Luna, existing credit only; three-request/$1 upper bounds | No purchase/top-up; all three generation attempts HTTP429, cap exhausted; successful live evaluation remains open |
| Assessment repository acceptance | Existing project repository plus a separate upstream fork | If the assessed repository itself must be the fork, confirm this arrangement with the coordinator |

The separate fork exists and allows the local source/build checkpoint to proceed. The submission date and manual reviewer role are confirmed. Coordinator interpretation and independent PR approval, if required, remain visible dependencies; they do not authorize external messaging or fabricated approvals. The original 17 October planning window was one day before the then-stated submission date. Work continued on 22 October at the user's direction. Actual execution dates and remaining assessment dependencies are reported honestly; no coordinator deadline extension or acceptance is assumed.

Do not publish private reports, user identifiers, credentials, source snippets in API payloads, or program-confidential material. Preserve public upstream license/copyright notices in the imported source. New project records omit personal names and email addresses.

Optional Falco and policy explanation features wait until core requirements pass. Follow [requirements-checklist.md](requirements-checklist.md) for acceptance status.

Review reference: [GitHub required-review documentation](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews) distinguishes author self-review from an approving PR review.

## Current operating decision

The acknowledgement is confirmed. The user directed completing the study implementation before fixing vulnerabilities; every critical/high issue alias is retained for later remediation. Operational failures and missing evidence are still reported honestly. Current implementation, draft PRs and report status are in [project-completion.md](project-completion.md). Successful live AI evaluation and genuine independent review remain distinct from implementation completion. See [AI evaluation limits](ai-evaluation.md).

The later critical-remediation request supersedes critical-risk deferral: current source and image scans have zero critical findings, and the aggregate rejects any returning critical count. High/lower risks remain deferred. Changes are committed/pushed (`8ac412e`, `1616f14`), all eight hosted jobs pass with zero critical findings, the detailed Actions Summary is published, and the owned study deployment is updated; no production deployment or new API purchase occurred. [Repair scope and limitations](critical-remediation.md).
