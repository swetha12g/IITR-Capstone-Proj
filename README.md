# IITR Capstone Project

PipelineFortress — Secure CI/CD with GenAI-Assisted Triage.

The detailed execution roadmap is available in [docs/PipelineFortress_Detailed_Roadmap.pdf](docs/PipelineFortress_Detailed_Roadmap.pdf).

Status as of 17 October 2026: Day 1 setup and pinned Juice Shop baseline build/tests passed. Selected tests: 2,334 passed, 8 upstream skips, 0 failures; lint passed. The container/deployment, six-stage security pipeline, AI triage, and final assessment work remain pending.

- [Execution guide](10-days-work-break-down.md)
- [Day 1 checkpoint](docs/day1-checkpoint.md)
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
