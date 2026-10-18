# IITR Capstone Project

PipelineFortress — Secure CI/CD with GenAI-Assisted Triage.

The detailed execution roadmap is available in [docs/PipelineFortress_Detailed_Roadmap.pdf](docs/PipelineFortress_Detailed_Roadmap.pdf).

Status as of 18 October 2026: Day 1 setup and pinned Juice Shop baseline build/tests passed. Selected tests: 2,334 passed, 8 upstream skips, 0 failures; lint passed. Day 2 source image and local kind deployment now pass runtime checks; [hosted CI passed](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/38957969793). Day 2 is complete, with the earlier deployment incident limitation recorded in its checkpoint. The six-stage security pipeline, AI triage, and final assessment remain pending.

- [Execution guide](10-days-work-break-down.md)
- [Day 1 checkpoint](docs/day1-checkpoint.md)
- [Day 2 checkpoint and lab commands](docs/day2-checkpoint.md)
- [Confirmed runtime baseline](docs/runtime-baseline.md)
- [Daily log and 18 October JIRA-style checklist](docs/daily-log.md)
- [Versions and local runtime selection](docs/versions.md)
- [Upstream fork/source provenance](docs/upstream-provenance.md)
- [Evidence and remaining requirements](docs/evidence-index.md)

After preparing the recorded user-local Node and Python environments, reproduce the selected local checks from Bash:

```bash
source scripts/dev-env.sh
python scripts/run-day1-checks.py
```

The runner uses the pinned imported source and recorded dependency locks. It keeps raw output in ignored private evidence and writes sanitized status manifests. It does not create a cluster or run live LLM calls. Juice Shop is an intentionally vulnerable lab target; a successful baseline build is not a production-safety claim.

Day 3 is complete for its source-scan/gate scope: [CI run 39111621696 passed](https://github.com/swetha12g/IITR-Capstone-Proj/actions/runs/39111621696), including 25 gate contracts, five rollout regressions, application build/tests, deployment/runtime and cleanup. All 221 findings remain visible; 186 exact lab-only risks are approved until 25 October 2026 at 00:00 IST, with zero remaining blockers/errors. A deployment readiness race was fixed and verified. Accepted risk is not remediation or production readiness. Day 4 awaits the program acknowledgement; assistance is requested. See [Day 3 checkpoint](docs/day3-checkpoint.md) and [daily checklist](docs/daily-log.md).
