"""adapt_span — converts an OpenInference span dict into a RECORD dict.

Key mappings (OpenInference → RECORD):
  span["context"]["span_id"]           → openinference_span_id
  span["attributes"]["input.value"]    → prompt
  span["attributes"]["output.value"]   → final_action.disposition
  span["attributes"]["llm.model_name"] → model_id
  span["attributes"]["metadata.*"]     → forwarded to matching RECORD fields
  child spans with span_kind=TOOL      → tools_accessed / tool_results
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


def adapt_span(span: dict[str, Any]) -> dict[str, Any]:
    """Convert an OpenInference span dict to a minimal RECORD dict.

    Fields not derivable from the span (authority_basis, agent_id, etc.)
    must be supplied via span metadata attributes or merged in by the caller.
    """
    attrs: dict = span.get("attributes", {})
    ctx: dict = span.get("context", {})
    meta: dict = {
        k.removeprefix("metadata."): v
        for k, v in attrs.items()
        if k.startswith("metadata.")
    }

    record: dict[str, Any] = {
        "record_id": meta.get("record_id") or str(uuid.uuid4()),
        "timestamp": _iso(span.get("start_time")),
        "agent_id": meta.get("agent_id") or span.get("name", "unknown-agent"),
        "agent_version": meta.get("agent_version", "0.0.0"),
        "authority_basis": meta.get("authority_basis", ["unknown.unknown"]),
        "operating_domain": meta.get("operating_domain", "supervised"),
        "prompt": attrs.get("input.value", ""),
        "final_action": {
            "type": meta.get("final_action_type", "respond"),
            "disposition": attrs.get("output.value", ""),
            "escalated": bool(meta.get("escalated", False)),
        },
    }

    if span_id := ctx.get("span_id"):
        record["openinference_span_id"] = span_id

    if model := attrs.get("llm.model_name"):
        record["model_id"] = model

    if jurisdiction := meta.get("jurisdiction"):
        record["jurisdiction"] = jurisdiction

    # chain_of_thought from llm.messages
    messages: list[dict] = attrs.get("llm.output_messages", [])
    thoughts = [
        {"step": i + 1, "content": m.get("message.content", ""), "type": "conclusion"}
        for i, m in enumerate(messages)
        if m.get("message.role") == "assistant"
    ]
    if thoughts:
        record["chain_of_thought"] = thoughts

    # tools from child spans of kind TOOL
    tool_spans: list[dict] = [
        s for s in span.get("child_spans", [])
        if s.get("span_kind") == "TOOL"
    ]
    if tool_spans:
        record["tools_accessed"] = [
            {
                "tool_name": s.get("name", "unknown"),
                "timestamp": _iso(s.get("start_time")),
                "query": s.get("attributes", {}).get("input.value", ""),
            }
            for s in tool_spans
        ]
        record["tool_results"] = [
            {
                "tool_name": s.get("name", "unknown"),
                "payload": s.get("attributes", {}).get("output.value", ""),
            }
            for s in tool_spans
        ]

    return record


def _iso(value: Any) -> str:
    """Return an ISO 8601 UTC string from a timestamp value or now()."""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1e9, tz=timezone.utc).isoformat()
    if isinstance(value, str) and value:
        return value
    return datetime.now(timezone.utc).isoformat()
