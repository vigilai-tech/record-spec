"""GapAnalyzer — per-regulation compliance scoring for RECORD traces."""

from __future__ import annotations

from typing import Any

_REGULATIONS: dict[str, dict] = {
    "fincen_nprm_2026": {
        "name": "FinCEN AML NPRM 2026",
        "required": [
            {
                "field": "authority_basis",
                "article": "§1010.230",
                "reason": "Machine-readable reference to the AML programme requirement the decision addresses",
            },
            {
                "field": "influencing_parameters",
                "article": "§1010.210",
                "reason": "Transaction attributes that triggered the suspicious-activity disposition must be retained",
            },
            {
                "field": "data_at_decision",
                "article": "§1010.210",
                "reason": "Data sources and integrity hashes proving the AI acted on accurate, unaltered data",
            },
            {
                "field": "tools_accessed",
                "article": "§1010.210",
                "reason": "Data-access patterns — sanctions screens, customer profiles, SWIFT parser calls",
            },
            {
                "field": "tool_results",
                "article": "§1010.210",
                "reason": "Payloads the agent received from each data source, required for examiner review",
            },
            {
                "field": "decision_lineage",
                "article": "§1010.320",
                "reason": "Case ID linking the RECORD trace to the operational AML case and SAR filing",
            },
            {
                "field": "outcome_linkage",
                "article": "§1010.320",
                "reason": "Closed-loop proof that AML monitoring produced an actionable outcome (SAR or documented no-file)",
            },
            {
                "field": "final_action",
                "article": "§1010.320",
                "reason": "Decision type and escalation record proving the oversight pathway functioned",
            },
        ],
        "recommended": [
            {
                "field": "human_disposition",
                "article": "§1010.320",
                "reason": "SAR filing decisions should document human review and analyst rationale",
            },
            {
                "field": "chain_of_thought",
                "article": "§1010.230",
                "reason": "Reasoning steps allow examiners to verify the AI programme meets minimum effectiveness criteria",
            },
            {
                "field": "policy_evaluation",
                "article": "§1010.230",
                "reason": "Per-rule verdicts demonstrate the AML policy ruleset was systematically applied",
            },
        ],
    },
    "eu_ai_act_art86": {
        "name": "EU AI Act Art. 86 (Right of Explanation)",
        "required": [
            {
                "field": "record_id",
                "article": "Art. 12(1)",
                "reason": "Unique identifier enabling point-in-time retrieval for explanation requests",
            },
            {
                "field": "timestamp",
                "article": "Art. 12(1)(a)",
                "reason": "Timestamped logging of AI system outputs",
            },
            {
                "field": "agent_id",
                "article": "Art. 13(3)(a)",
                "reason": "Identity of the AI system responsible for the decision",
            },
            {
                "field": "agent_version",
                "article": "Art. 12(1)(c)",
                "reason": "Version pinning for reproducibility and change management",
            },
            {
                "field": "schema_version",
                "article": "Art. 12(1)(c)",
                "reason": "Schema version ensures log records remain interpretable as the standard evolves",
            },
            {
                "field": "prompt",
                "article": "Art. 12(1)(b)",
                "reason": "Verbatim input capture — the single most important reproducibility artefact",
            },
            {
                "field": "chain_of_thought",
                "article": "Art. 13(3)(d)",
                "reason": "Interpretability: outputs must be comprehensible to deployer oversight personnel",
            },
            {
                "field": "influencing_parameters",
                "article": "Art. 13(3)(d)",
                "reason": "Principal factors driving the decision with quantified weights",
            },
            {
                "field": "operating_domain",
                "article": "Art. 14",
                "reason": "Human oversight level declaration required for high-risk AI systems",
            },
            {
                "field": "authority_basis",
                "article": "Art. 86(1)",
                "reason": "Machine-readable audit chain to the regulatory mandate that drove the decision",
            },
        ],
        "recommended": [
            {
                "field": "model_id",
                "article": "Art. 13(3)(a)",
                "reason": "Foundation model identifier for technical documentation",
            },
            {
                "field": "policy_evaluation",
                "article": "Art. 12(1)(b)",
                "reason": "Structured policy verdicts demonstrating systematic rule application",
            },
            {
                "field": "human_disposition",
                "article": "Art. 14(4)",
                "reason": "Evidence that human oversight personnel exercised their intervention right",
            },
            {
                "field": "data_at_decision",
                "article": "Art. 10(3)",
                "reason": "Data provenance and integrity proofs for data governance compliance",
            },
            {
                "field": "jurisdiction",
                "article": "Art. 2",
                "reason": "Jurisdictional scoping for multi-jurisdictional deployments",
            },
        ],
    },
    "mifid2_rts6": {
        "name": "MiFID II RTS 6 (Algorithmic Trading)",
        "required": [
            {
                "field": "timestamp",
                "article": "Art. 10(1)",
                "reason": "Timestamp granularity sufficient to reconstruct intraday order-flow context",
            },
            {
                "field": "agent_id",
                "article": "Art. 10(2)",
                "reason": "Identity of the algorithmic system responsible for the order",
            },
            {
                "field": "agent_version",
                "article": "Art. 10(2)",
                "reason": "Version of the algorithm logic applied to each order",
            },
            {
                "field": "prompt",
                "article": "Art. 10(1)",
                "reason": "Input instruction to the algorithmic system — required for reproducibility",
            },
            {
                "field": "policy_evaluation",
                "article": "Art. 10(1)(d)",
                "reason": "Pre-trade controls evaluated and their outcomes must be logged per order",
            },
            {
                "field": "tools_accessed",
                "article": "Art. 10(1)",
                "reason": "External data feeds accessed during order evaluation (L2, participant profile)",
            },
            {
                "field": "data_at_decision",
                "article": "Art. 10(1)",
                "reason": "Tamper-evident data provenance for each external feed used in the decision",
            },
            {
                "field": "final_action",
                "article": "Art. 10(1)",
                "reason": "Disposition and severity score required for alert-prioritisation audit trail",
            },
        ],
        "recommended": [
            {
                "field": "influencing_parameters",
                "article": "Art. 10(1)",
                "reason": "Quantified feature weights supporting model performance monitoring over time",
            },
            {
                "field": "chain_of_thought",
                "article": "Art. 10(1)",
                "reason": "Analytical steps allowing reconstruction of the intraday decision sequence",
            },
            {
                "field": "decision_lineage",
                "article": "Art. 10(1)",
                "reason": "Links the RECORD trace to the upstream surveillance alert and case ticket",
            },
            {
                "field": "openinference_span_id",
                "article": "Art. 10(1)",
                "reason": "Correlation with OTel observability trace for latency and performance audit",
            },
        ],
    },
    "sr_11_7": {
        "name": "Federal Reserve SR 11-7 (Model Risk Management)",
        "required": [
            {
                "field": "agent_id",
                "article": "§Model Inventory",
                "reason": "Every model must be catalogued with a stable identifier",
            },
            {
                "field": "agent_version",
                "article": "§Change Management",
                "reason": "Model version required to track changes through dev → validation → production",
            },
            {
                "field": "model_id",
                "article": "§Model Inventory",
                "reason": "Foundation model identifier required for inventory and vendor risk assessment",
            },
            {
                "field": "prompt",
                "article": "§Model Documentation",
                "reason": "Complete input specification — SR 11-7 mandates description of all model inputs",
            },
            {
                "field": "influencing_parameters",
                "article": "§Model Documentation",
                "reason": "Input variables and relative importance required in model documentation",
            },
            {
                "field": "chain_of_thought",
                "article": "§Model Documentation",
                "reason": "Intermediate reasoning enabling model validation and performance review",
            },
            {
                "field": "policy_evaluation",
                "article": "§Ongoing Monitoring",
                "reason": "Per-rule verdicts enable tracking model performance and detecting systematic weaknesses",
            },
            {
                "field": "final_action",
                "article": "§Use",
                "reason": "Model output record — severity score enables score-distribution tracking over time",
            },
        ],
        "recommended": [
            {
                "field": "data_at_decision",
                "article": "§Data Quality",
                "reason": "Evidence that model inputs met data-quality standards at decision time",
            },
            {
                "field": "decision_lineage",
                "article": "§Audit Trail",
                "reason": "Multi-step pipeline traceability from final decision back to originating alert",
            },
            {
                "field": "human_disposition",
                "article": "§Use and Ongoing Monitoring",
                "reason": "Human override records required to assess whether model outputs were used appropriately",
            },
            {
                "field": "outcome_linkage",
                "article": "§Ongoing Monitoring",
                "reason": "Closed-loop outcomes enable tracking whether model escalations produced correct results",
            },
            {
                "field": "schema_version",
                "article": "§Change Management",
                "reason": "Schema versioning ensures audit records remain interpretable across model versions",
            },
        ],
    },
}

KNOWN_REGULATIONS = list(_REGULATIONS)


def _present(doc: dict[str, Any], field: str) -> bool:
    if field not in doc:
        return False
    val = doc[field]
    return val not in (None, [], {}, "")


class GapAnalyzer:
    """Evaluates a RECORD document against a specific regulation's field requirements.

    Args:
        regulation: One of the regulation IDs in ``KNOWN_REGULATIONS``.

    Raises:
        ValueError: If *regulation* is not recognised.
    """

    def __init__(self, regulation: str) -> None:
        if regulation not in _REGULATIONS:
            known = ", ".join(KNOWN_REGULATIONS)
            raise ValueError(
                f"Unknown regulation {regulation!r}. Known: {known}"
            )
        self._reg_id = regulation
        self._reg = _REGULATIONS[regulation]

    def analyze(self, doc: dict[str, Any]) -> dict[str, Any]:
        """Return a compliance report dict for *doc*."""
        required_results = [
            {
                "field": f["field"],
                "present": _present(doc, f["field"]),
                "article": f["article"],
                "reason": f["reason"],
            }
            for f in self._reg["required"]
        ]
        recommended_results = [
            {
                "field": f["field"],
                "present": _present(doc, f["field"]),
                "article": f["article"],
                "reason": f["reason"],
            }
            for f in self._reg["recommended"]
        ]

        req_total = len(required_results)
        req_present = sum(1 for r in required_results if r["present"])
        score = (req_present / req_total * 100) if req_total else 100.0

        if score == 100.0:
            status = "COMPLIANT"
        elif score >= 60.0:
            status = "PARTIAL"
        else:
            status = "NON-COMPLIANT"

        return {
            "regulation": self._reg_id,
            "regulation_name": self._reg["name"],
            "score": score,
            "status": status,
            "required": required_results,
            "recommended": recommended_results,
        }
