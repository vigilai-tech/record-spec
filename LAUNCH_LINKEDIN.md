# LinkedIn Launch Post

---

AI agents are making credit decisions, triaging AML alerts, and dispositing trade surveillance cases at scale. But when examiners ask "show me why the model decided that" — most firms reach for spreadsheets.

We've published **RECORD** (Regulatory Evidence Capture of Reasoning and Decisions), a free, open JSON schema that gives every AI agent decision a structured audit trail from the start.

A RECORD trace captures what regulators actually ask for:

- **Which rule was evaluated** — and did it pass or fail (MiFID II RTS 6, SR 11-7)
- **What data the model saw** — with cryptographic hashes for tamper-evidence (EU AI Act Art. 12, SOX §302)
- **Why each factor mattered** — feature weights that map directly to ECOA §202.9 adverse-action reasons
- **What the human did** — override, confirm, or abstain, with a timestamped rationale (EU AI Act Art. 14)
- **Where the decision landed** — SAR filed, alert escalated, limit adjusted (FinCEN AML NPRM 2026)

Every field is mapped to a specific regulatory article in the accompanying documentation. Three reference examples are included: trade surveillance, AML wire-transfer triage, and a credit limit decision with a human override.

The schema is Apache 2.0, built as an extension to the OpenInference observability standard, and includes a Python SDK under 300 lines.

**https://github.com/[your-org]/record-spec**

For compliance officers and model risk teams building governance frameworks for AI: what's the single biggest gap in your current audit trail — the reasoning, the data provenance, or the human-in-the-loop record?
