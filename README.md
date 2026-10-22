# IITR Capstone Project

PipelineFortress — Secure CI/CD with GenAI-Assisted Triage.

The detailed execution roadmap is available in [docs/PipelineFortress_Detailed_Roadmap.pdf](docs/PipelineFortress_Detailed_Roadmap.pdf).

Status on 22 October 2026: the complete local six-stage security pipeline passes execution with deferred findings. The hardened source-built image, passive ZAP coverage, deduplicated dashboard, source-free AI boundary and three focused remediation examples have real local evidence. The current offline application profile passes 2,326 tests with seven skips; nine external-service availability tests are excluded explicitly. See [current completion state](docs/project-completion.md) for hosted, reproduction and review status.

The user directed finishing the study implementation and fixing vulnerabilities later. All critical/high issue aliases are retained in the [deferred register](docs/deferred-remediation.md). Scanner errors, missing stages and invalid reports remain execution errors. All three bounded OpenAI generation attempts returned HTTP429; no successful live triage is claimed. No API purchase, top-up or further automatic attempt is made.

- [Dashboard](reports/sanitized/dashboard/index.html)
- [Twelve-page study report](output/pdf/PipelineFortress_Study_Report.pdf)
- [Reproduction instructions](docs/reproduction.md)
- [Review ledger](docs/reviews.md)
- [Defense notes](docs/defense.md)

- [Execution guide](10-days-work-break-down.md)
- [Day 1 checkpoint](docs/day1-checkpoint.md)
- [Day 2 checkpoint and lab commands](docs/day2-checkpoint.md)
- [Confirmed runtime baseline](docs/runtime-baseline.md)
- [Daily log and 18 October JIRA-style checklist](docs/daily-log.md)
- [Versions and local runtime selection](docs/versions.md)
- [Upstream fork/source provenance](docs/upstream-provenance.md)
- [Evidence and remaining requirements](docs/evidence-index.md)

To reproduce in a separate full-history clone with Docker and Python 3.10:

```bash
bash scripts/reproduce.sh
```

This bootstraps project-local tools, uses an owned temporary cluster, retains sanitized receipts and performs mock AI triage without API spending. Raw scanner reports, credentials, full SBOMs and private logs stay ignored. Juice Shop remains intentionally vulnerable. [Historical Day 3 CI](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696) and its exact expiring source approvals are retained separately; the new study workflow is the automatic execution path, while the historical strict workflow is manual.
