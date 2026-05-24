# RECORD — Regulatory Mapping

This document maps every RECORD schema field to the specific regulatory obligations that motivate its capture. Compliance teams should use this table to demonstrate that a RECORD-instrumented system satisfies the evidence-preservation requirements of each cited framework.

**Scope:** Trade surveillance + AML/communications surveillance.

---

## Field-by-Field Regulatory Mapping

## 1. Unique Records & Metadata

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `record_id` | Art. 12(1) | — | — | 17a-4(a) | 4511 | 1010.430 |
| `timestamp` | Art. 12(2)(a) | Art. 16(7); RTS 6 Art. 28; RTS 25 | — | 17a-4(a) | — | 1010.430 |
| `agent_id` | Art. 13(3)(a) | — | — | — | 3110 | — |
| `agent_version` | Art. 13(3)(c) | RTS 6 Art. 11 | — | — | — | 1010.210 |
| `operating_domain` | Art. 14; Art. 26(5) | RTS 6 Art. 1 | — | — | — | 1010.210 |

## 2. Explainability & Parameters

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `influencing_parameters.factor` | Art. 13(3)(d) | — | — | — | 3110 | 1010.320 |
| `influencing_parameters.value` | Art. 12(2)(b) | — | — | — | — | — |
| `influencing_parameters.weight` | Art. 13(3)(d) | — | — | — | — | — |

## 3. Rule Enforcement & Verdicts

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `policy_evaluation.rule_id` | Art. 12(1) | RTS 6 Art. 15 | — | — | — | 1010.210 |
| `policy_evaluation.rule_name` | Art. 13(1) | — | — | — | — | — |
| `policy_evaluation.verdict` | Art. 12(2)(b) | RTS 6 Art. 15 | — | — | — | 1010.320 |
| `policy_evaluation.confidence` | Art. 13(3)(d) | — | — | — | — | — |

## 4. Traceability & Lineage

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `decision_lineage.parent_trace_id` | Art. 12(1) | — | — | 17a-4(b) | 4511 | 1010.430 |
| `decision_lineage.case_id` | — | — | Art. 16 | — | — | 1010.320 |
| `decision_lineage.investigation_thread_id` | Art. 12(1) | — | Art. 16 | — | — | 1010.320 |

## 5. Point-in-Time Data Capture

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `data_at_decision.source` | Art. 10(3) | RTS 6 Art. 11 | — | — | — | 1010.210 |
| `data_at_decision.query` | Art. 12(2)(b) | RTS 6 Art. 28 | — | — | — | 1010.430 |
| `data_at_decision.payload_hash` | Art. 12(2)(b) | RTS 6 Art. 28 | — | 17a-4(f) | — | 1010.430 |
| `data_at_decision.payload_preview` | Art. 13(1) | — | — | — | — | — |

## 6. Human Oversight & Manual Interventions

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `human_disposition.action` | Art. 14(4)(d) | RTS 6 Art. 1 | — | — | 3110 | 1010.320 |
| `human_disposition.rationale` | Art. 14(4) | — | — | — | 3110 | 1010.320 |
| `human_disposition.analyst_id` | Art. 26(2) | — | — | 17a-4(a) | 3110 | 1010.430 |
| `human_disposition.reviewed_at` | — | RTS 6 Art. 16 | — | 17a-4(a) | 4511 | 1010.430 |

## 7. Downstream Accountability & Outcomes

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `outcome_linkage.type` | — | — | Art. 16 | — | — | 1010.320 |
| `outcome_linkage.reference_id` | — | — | Art. 16 | 17a-4(b) | 4511 | 1010.320; 1010.430 |
| `outcome_linkage.status` | Art. 12(1) | — | — | — | 3110 | — |

## 8. Verbatim Inputs & Intermediates

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `prompt` | Art. 12(2)(b) | RTS 6 Art. 11 | — | — | — | 1010.430 |
| `chain_of_thought.content` | Art. 13(3)(d) | — | — | — | — | 1010.320 |
| `chain_of_thought.type` | Art. 13(1) | — | — | — | — | — |

## 9. Tool Calls & External APIs

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `tools_accessed.tool_name` | Art. 12(2)(b) | RTS 6 Art. 11 | — | — | — | 1010.210 |
| `tools_accessed.timestamp` | Art. 12(2)(a) | RTS 25 | — | 17a-4(a) | — | 1010.430 |
| `tools_accessed.query` | Art. 12(2)(b) | RTS 6 Art. 28 | — | — | — | 1010.430 |
| `tool_results.payload` | Art. 12(2)(b) | — | — | — | — | 1010.210 |

## 10. Actions, Severity & Escalations

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `final_action.type` | Art. 12(2)(b) | RTS 6 Art. 28 | Art. 16 | — | — | 1010.320 |
| `final_action.disposition` | Art. 13(1) | — | Art. 16 | — | 3110 | 1010.320 |
| `final_action.severity_score` | Art. 13(3)(d) | RTS 6 Art. 15 | — | — | — | 1010.210 |
| `final_action.escalated` | Art. 14(4)(e) | — | Art. 16 | — | — | 1010.320 |
| `final_action.escalation_reason` | Art. 14(4) | — | Art. 16 | — | — | 1010.320 |

## 11. System Observability, IDs & Schemas

| Field | EU AI Act | MiFID II / RTS | MAR | SEC 17a-4 | FINRA | BSA / FinCEN |
|---|---|---|---|---|---|---|
| `openinference_span_id` | Art. 12(1) | — | — | 17a-4(f) | — | 1010.430 |
| `model_id` | Art. 11 + Annex IV | — | — | — | — | — |
| `jurisdiction` | Art. 2 | Art. 1 | — | — | — | AMLA 2020 / 31 USC 5311 |
| `schema_version` | Art. 13(3)(f) | RTS 6 Art. 11 | — | — | — | 1010.210 |

---

## Retention Floors

Apply across all logged fields:

- **EU AI Act Art. 26(6)** — 6 months minimum for high-risk AI system logs
- **BSA 31 CFR 1010.430** — 5 years
- **SEC 17a-4** — 3–6 years depending on record type; 17a-4(f) imposes WORM or audit-trail-alternative integrity requirements for electronic records
- **MiFID II / MiFIR Art. 25** — 5 years (extendable to 7 by competent authority)

## Context Notes

- **SR 26-2** (April 17, 2026): superseded SR 11-7. Explicitly excludes generative and agentic AI from formal MRM scope, leaving agentic governance under banks' enterprise risk frameworks. Cited here for context only — not a field-level anchor for the agent layer.
- **FinCEN Order FIN-2026-R001** (Feb 13, 2026): exceptive relief from the CDD/Beneficial Ownership re-verification requirement at each new account opening (31 CFR 1010.230). Shifts re-verification to risk-based triggers.
- **RTS 25** (Commission Delegated Regulation (EU) 2017/574) remains the current business-clock-synchronisation standard. A revised version is anticipated under MiFID II Art. 22c but is not yet in application.

## Glossary

- **EU AI Act** — Regulation (EU) 2024/1689
- **MiFID II** — Directive 2014/65/EU; **MiFIR** — Regulation (EU) 600/2014
- **RTS 6** — Commission Delegated Regulation (EU) 2017/589 (algorithmic trading organisational requirements)
- **RTS 25** — Commission Delegated Regulation (EU) 2017/574 (business clock synchronisation)
- **MAR** — Regulation (EU) 596/2014 (Market Abuse Regulation)
- **SEC 17a-4** — 17 CFR 240.17a-4 (broker-dealer recordkeeping)
- **FINRA 3110 / 4511** — Supervision / Books and records
- **BSA** — Bank Secrecy Act; **AMLA 2020** — Anti-Money Laundering Act of 2020
- **31 CFR 1010.210** — AML program requirements
- **31 CFR 1010.230** — Customer Due Diligence / Beneficial Ownership
- **31 CFR 1010.320** — Suspicious Activity Report filing
- **31 CFR 1010.430** — BSA recordkeeping (5-year retention)
