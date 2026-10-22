# AI evaluation status and limits

The configured external application client is OpenAI GPT-6 Luna at the official Responses endpoint. The user selected an existing external credential and declined any additional purchase. Three bounded, source-free generation attempts returned HTTP429 after a successful read-only model lookup. The specific cause was not established. The request cap is exhausted; no further automatic attempt, top-up or billing change is made.

## What was actually verified

- Final serialized mock HTTP bodies contain only the constructed allowlisted request and synthetic finding metadata. Private paths, source, matches, contacts and canaries are excluded.
- Unknown/free-text fields, malformed metadata and unverified versions refuse before transport, producing zero calls.
- The independent advisory catalog is derived from hash-bound raw scanner reports. Tampered reports fail, and a fresh run does not depend on the earlier private baseline catalog.
- Unknown or omitted IDs, incorrect issue clusters, invented CVEs/versions, unsupported operations and unsafe references are rejected by deterministic output validation.
- Twenty-finding deterministic mock triage passed. The three local patch templates also passed real selected-check and functional before/after verification.

These checks establish boundary/contract behavior, not real model accuracy. The [current test proof](../reports/sanitized/day7/redaction-tests.json) binds the relevant code/prompt hash and records the test count. Mock results remain labeled mock.

## Measurements that remain unavailable

No successful live model response was received. Consequently model precision/recall, model FP/FN rates, live correctness, hallucination/refusal frequency over an evaluation set, live latency distribution and actual returned token usage/cost are unavailable. Conservative budget reservations are not billed usage. The public failure receipt is [triage-live-error.json](../reports/sanitized/day8/triage-live-error.json).

The dashboard's 21-case detection evaluation measures scanner fixtures/controls, including one verified scanner miss. It is post-hoc and not independently labeled; it is not an AI-accuracy result. Three coding-assistant-authored draft proposals are real, but the unavailable external API is not credited with generating them. Independent human review and first-review correctness remain unmeasured.

If the user later supplies a working authorized access path, preregister an independent sample and scoring criteria before a new live evaluation. Do not reset the existing ledger, invent successful outputs or use another provider without authorization. The present implementation/report can be assessed with this limitation recorded.
