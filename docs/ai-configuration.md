# Live AI configuration — OpenAI selected; generation unavailable

On 22 October 2026 the user explicitly selected the OpenAI API credential in an external local file and instructed using OpenAI instead of any Claude credential. The implementation will use **GPT-6 Luna**, the recommended OpenAI option, with a **$1 total application cap** as proposed in the selection. No credential value or sensitive file contents are recorded here. Anthropic credentials/endpoints are excluded from this integration. Credential/model read-only validation and captured-body safeguards precede any generated triage request.

**Billing constraint:** the user explicitly declined any new purchase. The proposed dollar amount is a usage ceiling, not a payment request. Use existing available credit only; do not buy credits, top up, enable billing or change account billing settings. Keep the real evaluation small and bounded. If the provider rejects existing access/credit, retain the real failure honestly and continue all independent project work.

**Observed access:** read-only lookup of GPT-6 Luna succeeded with HTTP200. All three bounded source-free generation attempts returned HTTP429; the more specific cause was not established. No successful generation, actual token usage or invoice cost is claimed. The conservative reservations total approximately $0.0045; reservations are not billed usage. The three-request cap is exhausted and no further automatic requests are made. Mock triage is explicitly labeled mock. Existing credential contents remain outside the repository and Claude credentials were not used.

Official options checked on that date, standard USD prices per million tokens:

| Option | Model | Input / output | Proposed application limit |
|---|---|---|---|
| A, recommended for this small pilot | [OpenAI GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) | $0.10 / $0.50 | $1 total, only after user selection |
| B | [Gemini 3.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.5-flash-lite) | Eligible free tier; paid $0.30 / $2.50 | Free-tier-only use, no paid usage |
| C | [Claude Haiku 5.5](https://platform.claude.com/docs/en/about-claude/pricing) | $0.10 / $0.50 for prompts up to 100,000 tokens | $1 total, only after user selection |

Published availability is not proof of account-specific access. Google identifies free-tier content as eligible for product improvement; only allowlisted, source-free metadata may leave the lab regardless of provider. Credentials must be configured privately and never copied into project Markdown, logs, reports, commits or chat. A proposed budget is not spending authorization. Minimum provider funding, account limits and actual token usage are separate from this application cap.

Next: continue independent local/reproduction/report work. Preserve the three real failure receipts and exhausted cap; do not retry automatically or buy credit. A successful live evaluation remains open unless the user later provides a working authorized access path. [API authentication guidance](https://developers.openai.com/api/reference/overview#authentication).
