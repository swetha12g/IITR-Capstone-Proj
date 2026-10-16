# PipelineFortress operating scope

Updated: 17 October 2026.

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
| API provider/model and spend cap | Pending | Day 1 uses no live LLM API; later live work waits for safeguards and explicit configuration |
| Assessment repository acceptance | Existing project repository plus a separate upstream fork | If the assessed repository itself must be the fork, confirm this arrangement with the coordinator |

The separate fork exists and allows the local source/build checkpoint to proceed. The submission date and manual reviewer role are confirmed. Coordinator interpretation and independent PR approval, if required, remain visible dependencies; they do not authorize external messaging or fabricated approvals. The deadline is one calendar day after this execution date, while the six-stage pipeline, AI safeguards/evaluation, remediation PRs, and final report remain unimplemented. No claim is made that the full ten-day scope can be completed by that date.

Do not publish private reports, user identifiers, credentials, source snippets in API payloads, or program-confidential material. Preserve public upstream license/copyright notices in the imported source. New project records omit personal names and email addresses.

Optional Falco and policy explanation features wait until core requirements pass. Follow [requirements-checklist.md](requirements-checklist.md) for acceptance status.

Review reference: [GitHub required-review documentation](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews) distinguishes author self-review from an approving PR review.
