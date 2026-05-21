"""RecordEmitter — builds and persists RECORD trace documents."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RecordEmitter:
    """Builds RECORD dicts from agent metadata + per-call fields and appends
    them to a .jsonl sink.

    Args:
        agent_id: Stable identifier for the agent system.
        agent_version: Semantic version of the agent.
        authority_basis: Regulatory dot-notation strings, e.g. ``["mifid2.rts6"]``.
        operating_domain: ``"autonomous"``, ``"supervised"``, or ``"human_only"``.
        output_path: ``.jsonl`` file path; created if absent.
        model_id: Optional foundation-model identifier.
        jurisdiction: Optional ISO 3166-1 alpha-2 jurisdiction tag.
    """

    SCHEMA_VERSION = "0.1.0"

    def __init__(
        self,
        agent_id: str,
        agent_version: str,
        authority_basis: list[str],
        operating_domain: str,
        output_path: str | Path = "record_traces.jsonl",
        model_id: str | None = None,
        jurisdiction: str | None = None,
    ) -> None:
        if operating_domain not in {"autonomous", "supervised", "human_only"}:
            raise ValueError(f"Invalid operating_domain: {operating_domain!r}")
        self.agent_id = agent_id
        self.agent_version = agent_version
        self.authority_basis = authority_basis
        self.operating_domain = operating_domain
        self.output_path = Path(output_path)
        self.model_id = model_id
        self.jurisdiction = jurisdiction

    def emit(
        self,
        *,
        prompt: str,
        final_action: dict[str, Any],
        record_id: str | None = None,
        timestamp: str | None = None,
        influencing_parameters: list[dict] | None = None,
        policy_evaluation: list[dict] | None = None,
        decision_lineage: dict | None = None,
        data_at_decision: list[dict] | None = None,
        human_disposition: dict | None = None,
        outcome_linkage: dict | None = None,
        chain_of_thought: list[dict] | None = None,
        tools_accessed: list[dict] | None = None,
        tool_results: list[dict] | None = None,
        openinference_span_id: str | None = None,
    ) -> dict[str, Any]:
        """Build a RECORD dict, append it to the .jsonl file, and return it."""
        doc: dict[str, Any] = {
            "record_id": record_id or str(uuid.uuid4()),
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "schema_version": self.SCHEMA_VERSION,
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "authority_basis": self.authority_basis,
            "operating_domain": self.operating_domain,
            "prompt": prompt,
            "final_action": final_action,
        }

        optional = {
            "model_id": self.model_id,
            "jurisdiction": self.jurisdiction,
            "openinference_span_id": openinference_span_id,
            "influencing_parameters": influencing_parameters,
            "policy_evaluation": policy_evaluation,
            "decision_lineage": decision_lineage,
            "data_at_decision": data_at_decision,
            "human_disposition": human_disposition,
            "outcome_linkage": outcome_linkage,
            "chain_of_thought": chain_of_thought,
            "tools_accessed": tools_accessed,
            "tool_results": tool_results,
        }
        doc.update({k: v for k, v in optional.items() if v is not None})

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(doc, ensure_ascii=False) + "\n")

        return doc
