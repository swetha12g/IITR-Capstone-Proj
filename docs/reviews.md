# Remediation review ledger

The PR delivery and unmerged-draft statements below describe the original 22 October 2026 snapshot. On 31 October the user explicitly authorized merging the proposals and promoting a project release. See [release promotion](release-promotion.md) for verified progress. Owner-directed merging does not establish independent human approval or first-review correctness; those assessment requirements remain open.

The three focused proposals are authored by the Codex coding assistant using bounded local templates. The external triage API returned HTTP429 and is not credited with generating these plans. Each branch must target the integration branch independently. No automatic merge or review-request message is authorized by this ledger.

| Proposal | Change | Actual local verification | Independent review / first-review correctness |
|---|---|---|---|
| PF-001 | Disable service-account token mounting in the legacy baseline deployment | Selected Checkov check fails before, passes after; both deployments Ready and HTTP checks pass; namespace removed | Pending; not measured |
| PF-002 | Explicitly require non-root execution in the legacy baseline deployment | Same before/after evidence; baseline already ran UID65532, so this adds policy rather than removing an observed root process | Pending; not measured |
| PF-003 | Add the baseline liveness probe | Selected Checkov check fails before, passes after; both deployments Ready and HTTP checks pass; namespace removed | Pending; not measured |

Source: [sanitized verification](../reports/sanitized/day9/proposals.json). Private patches and raw reports remain ignored. Actual independent draft PRs: [PF-001](https://github.com/swetha12g/IITR-Capstone-Proj/pull/1), [PF-002](https://github.com/swetha12g/IITR-Capstone-Proj/pull/2), [PF-003](https://github.com/swetha12g/IITR-Capstone-Proj/pull/3). Each remains a one-file diff. Integration fixes were merged into each published branch without rewriting history, so each retains the original focused fix plus integration merge commits. No review requests or merges were made. The coding assistant's implementation checks are not an independent human approval. A real reviewer must record a date, verdict, requested changes and whether the first submitted revision was correct. No reviewer identity or approval is invented.

All three eight-job hosted workflows are green: [PF-001 verification](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39818848200), [PF-002 verification](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39818849061), [PF-003 verification](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39818848272). Observed review count is zero for each, and each remains an unmerged draft. [Sanitized PR receipt](../reports/sanitized/day9/pr-receipt.json) binds the actual tested heads.
