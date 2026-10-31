# Release promotion record

## Request and intended sequence

On 31 October 2026 IST, the user explicitly requested merging all open remediation PRs into `feature-16-kick-start`, then promoting to `develop` and `main`, creating a release tag and publishing release notes. The selected first project release tag is `v1.0.0`; no existing project tags were present.

The three originally selected proposals are PRs 1, 2 and 3, all targeting the integration branch. The changes disable unnecessary service-account token mounting, make non-root execution explicit and add a liveness probe. The adjacent YAML additions from PRs 1 and 2 require a mechanical conflict resolution that retains both controls. No existing runtime deployment is changed by merging repository files.

## Verification and publication policy

The release candidate is assembled in an isolated worktree. Existing tests and selected real Checkov controls validate the combined deployment manifest. The release-publication guard has negative tests for invalid tags, missing notes, wrong main identity, missing successful CI and API failure. Full hosted study CI runs on `feature-16-kick-start`, `develop` and `main`. The tag is created only after the final promoted main revision passes that workflow.

The tag workflow uses a pinned checkout action, no persisted checkout credentials, job-scoped contents write/actions read permissions and a finite timeout. It verifies the tag identifies current main and a successful push run exists for that exact commit before publishing the versioned notes. It uses the runner-provided token without inspecting or printing credentials. Branch protections and required checks are not bypassed; no force push is authorized or used.

The locally prepared `Final-Submission` package and pre-existing local documentation changes are preserved outside the publication candidate. This release adds only the requested merges, release automation, guard tests and release records. No application dependency version is changed to match the independent project tag.

## Preparation snapshot

At this preparation snapshot, [PR 1](https://github.com/swetha12g/IITR-Capstone-Proj/pull/1) is verified merged as `4280b07e5ff91cc4b57b2cb4378439eeaf6dadf6`. PR 2 has a verified non-force conflict-resolution push at `501f94fa1ab25766b300430765614e8e3c2facac`, retaining both pod controls, and [fresh CI](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/41178710012) is in progress. PR 3, promotions, final main CI, tag and release publication are not yet claimed complete in this snapshot. Later results require readback from the PRs, Actions and release page.

The isolated candidate passes 125 local contracts and all three selected Checkov checks with no skips or parsing errors. Native adversarial review found no remaining actionable code defects after tag provenance and retry-safety repairs. Coverage review records remaining local fail-closed edge cases and the pending hosted user flow rather than claiming exhaustive coverage. The shipping log/gate helpers could not run because Bun is absent; no installation or helper-success claim is made. Native review, real Checkov, shell/workflow parsing and hosted verification supply the actual check evidence.

Independent human review, successful live AI evaluation, independent detection labels and genuine oral/program acceptance remain open assessment requirements. Owner-directed merging is authorized repository work and does not close those evidence gaps.
