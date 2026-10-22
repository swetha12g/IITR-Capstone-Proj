# Demonstration and oral-defense notes

Prepared sequence for an eight-to-ten-minute demonstration. A live rehearsal with the assessor has not occurred; this is a runnable guide, not evidence of a completed oral defense.

| Time | Demonstration | Evidence / honest boundary |
|---|---|---|
| 0–1 min | Explain the owned training target and six scanner stages | Architecture in the report; no production-safety claim |
| 1–2 min | Show offline build/test receipt and exact image linkage | 2,326 application tests passed, seven skipped, nine external availability tests omitted |
| 2–3 min | Explain strict versus study execution | Findings deferred by the project owner; missing scans and invalid artifacts remain errors |
| 3–4 min | Show hardened runtime and image/SBOM comparison | Seven expected behaviors; UID/capabilities/read-only checks; full CIS coverage not claimed |
| 4–5 min | Open the dashboard and show a known miss | Post-hoc curated fixture metrics; labels not independently reviewed |
| 5–6 min | Run redaction/refusal and grounding tests | `source scripts/dev-env.sh`, then `python -m pytest tests/redaction tests/triage -q` |
| 6–7 min | Show an actual bounded proposal and before/after evidence | Coding-assistant authorship; external application API did not generate it |
| 7–8 min | Show reproduction receipt, report and risk backlog | Raw data stays private; no live API purchase or top-up |
| 8–10 min | Discuss limitations and answer questions | HTTP429 live triage, pending independent review, limited DAST, deferred defects |

Use the retained sanitized evidence as the recorded-run fallback when network or registry access fails. Do not describe a fallback as a new live execution. Human review and first-review correctness are reported only when genuine review arrives.
