# IITR Capstone Project

PipelineFortress — Secure CI/CD with GenAI-Assisted Triage.

The detailed execution roadmap is available in [docs/PipelineFortress_Detailed_Roadmap.pdf](docs/PipelineFortress_Detailed_Roadmap.pdf).

Status on 23 October 2026: **critical repairs are committed and pushed; local and hosted scans confirm 11 → 0 critical findings** in fresh dependency and rebuilt-image scans. All six scanner stages, exact-image runtime checks and the existing owned study deployment pass. The selected application suites have 2,332 passes and six skips; nine external availability tests are excluded. [Critical remediation and verification](docs/critical-remediation.md).

The refreshed dashboard records 180 underlying issues: zero critical and 91 high; high/lower findings remain deferred. A new gate fails if a critical finding returns. Repairs are committed as `8ac412e` and the Actions report as `1616f14`. [Fresh hosted CI and the one-stop report](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39842575944) passed all eight jobs, with zero critical findings. The detailed Summary and downloadable report packet are published and checksum-verified; the earlier hosted pass predates this repair. See [current completion state](docs/project-completion.md) for publication and remaining assessment work.

The twelve-page report now includes accepted hosted repair proof and a fresh repaired checkout. The dashboard displays measured timing and API/review status; desktop/mobile visual checks pass. Three infrastructure draft PRs are delivered. Successful live OpenAI evaluation and genuine independent review remain open; the three bounded generation attempts returned HTTP429. No additional API call or purchase occurred during this repair.

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
