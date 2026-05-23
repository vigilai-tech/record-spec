# Show HN: RECORD – an open schema for AI agent decision audit trails in regulated industries

We're proposing an open standard called **RECORD** (Regulatory Evidence Capture of Reasoning and Decisions) and would love feedback from people building AI agents in finance, healthcare, or any regulated domain.

**The gap we're trying to close**

OpenInference and OpenTelemetry do a great job capturing *operational* telemetry: token counts, latency, retrieval scores, tool call durations. That's the right abstraction for observability engineers.

But when a financial firm deploys an LLM agent to triage AML alerts, disposition trade surveillance cases, or recommend credit decisions, regulators ask a completely different set of questions:

- Which regulation required this decision to be made, and can you prove the model evaluated the right rules?
- What data was present at the exact moment the model decided — and can you hash-verify it?
- Did a human review the output, override it, or confirm it, and why?
- What was the chain of reasoning, step by step?
- Where did this decision end up — was a SAR filed, was an alert escalated, was a loan declined?

None of this is in an OTel span. The result is that compliance teams are hand-rolling bespoke logging schemas — one per firm, none interoperable, all expensive to audit.

**What RECORD is**

RECORD is a JSON Schema (draft-07) that extends OpenInference by adding a structured "decision audit envelope" alongside an existing span. It's not a new observability pipeline — you emit a RECORD document as a sidecar to your existing traces.

Key fields:

- `authority_basis` — machine-readable regulatory citation (e.g. `"mifid2.rts6"`, `"ecoa_reg_b.s202_9"`) so a governance dashboard can filter records by obligation
- `policy_evaluation` — ordered log of each rule the agent evaluated, its verdict, and the model's confidence
- `influencing_parameters` — feature-level explainability with weights (satisfies ECOA §202.9 adverse-action reason requirements)
- `chain_of_thought` — verbatim intermediate reasoning steps, typed as observation / hypothesis / analysis / conclusion
- `data_at_decision` — SHA-256 hashes of every data source queried, so you can prove the model saw the correct data
- `human_disposition` — structured record of whether a human overrode, confirmed, or abstained
- `outcome_linkage` — pointer to the downstream artefact (the SAR, the escalation ticket, the credit adjustment)

Every field maps to a specific article in the EU AI Act, MiFID II RTS 6, FinCEN's 2026 AML NPRM, SR 11-7, ECOA Reg B, or SOX §302. That mapping is in `REGULATORY_MAPPING.md` in the repo.

**The Python SDK and CLI**

We included a small reference implementation (`record-py`, installable via pip) with two interfaces.

A CLI for validation and compliance gap analysis:

```bash
# Schema validation
record validate trace.json

# Per-regulation compliance scoring
record gap-analyze trace.json --regulation fincen_nprm_2026
record gap-analyze trace.json --regulation eu_ai_act_art86
record gap-analyze trace.json --regulation mifid2_rts6
record gap-analyze trace.json --regulation sr_11_7
```

The gap analyzer is the part we think matters most. It doesn't just tell you "valid" or "invalid" — it scores your trace field-by-field against a specific regulation and names every gap with the article that demands it:

```
Compliance Score:  87%  PARTIAL

Required Fields (7/8)
  ✓  authority_basis           §1010.230
  ✓  influencing_parameters    §1010.210
  ✗  data_at_decision          §1010.210
       Data sources and integrity hashes proving the AI acted on accurate, unaltered data
  ...
```

And an emitter API for teams building agents from scratch:

```python
emitter = RecordEmitter(
    agent_id="aml-triage-agent",
    agent_version="2.1.4",
    authority_basis=["fincen_aml_nprm_2026.s_1010_320"],
    operating_domain="supervised",
)
doc = emitter.emit(prompt=..., final_action=..., chain_of_thought=...)
```

There's also an `adapt_span()` function that converts an OpenInference span dict into a RECORD dict for teams already instrumented with OTel.

**Three realistic examples in the repo**

- MiFID II trade surveillance: L1 agent dispositions an AAPL layering alert (OTR 47.3, cancel ratio 91%), evaluates five RTS 6 rules, escalates to L2
- FinCEN AML: agent reviews a $47k wire to a Liechtenstein private bank, queries sanctions + customer history, drafts a SAR narrative
- MAR Art. 14 communication surveillance: agent detects insider tipping in a Bloomberg chat — cross-references deal-room access logs (bookkeeping), NLP-scored message content, and counterparty options flow (Apex Capital opened a $2.1M NVDA put position 32 minutes after the chat); all three MAR Art. 14(3) tipping elements satisfied, direct escalation to Legal with evidence preservation trigger

**What we're looking for**

This is a community proposal, not a product. We'd genuinely like:

1. Are there fields that matter for your domain that we've missed?
2. Are any of the regulatory citations wrong or outdated?
3. Should `authority_basis` be a controlled vocabulary or free-form?
4. Is there a cleaner way to handle the OpenInference integration?
5. Who else is working on this problem — should RECORD live under the OpenInference org?

Repo: https://github.com/[your-org]/record-spec (Apache 2.0, JSON Schema + Python SDK + examples)

Happy to dig into any of the regulatory specifics or the schema design in the comments.
