"""demo.py — emit one trade-surveillance RECORD trace and validate it."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from record_py import RecordEmitter, RecordValidator

emitter = RecordEmitter(
    agent_id="trade-surveillance-l1-agent",
    agent_version="3.2.1",
    authority_basis=["mifid2.rts6", "eu_ai_act.art_86"],
    operating_domain="supervised",
    output_path="/tmp/record_demo.jsonl",
)

doc = emitter.emit(
    prompt="Evaluate layering alert SURV-2026-DEMO-001 on AAPL. OTR=47.3, cancel_ratio=0.91.",
    final_action={"type": "escalate_l2", "disposition": "All RTS 6 rules fail. Escalating.", "severity_score": 8.4, "escalated": True},
    influencing_parameters=[{"factor": "order_cancel_ratio_5min", "value": 0.91, "weight": 0.32}],
    policy_evaluation=[{"rule_id": "RTS6-P1-CANCEL-RATE", "rule_name": "Excessive Order Cancellation Rate", "verdict": "fail", "confidence": 0.97}],
    chain_of_thought=[{"step": 1, "content": "Cancel ratio 91% far exceeds 60% threshold.", "type": "conclusion"}],
)

schema_path = Path(__file__).parent.parent.parent / "schema.json"
result = RecordValidator(schema_path).validate(doc)
print("PASS" if result["valid"] else "FAIL")
for err in result["errors"]:
    print(" ", err)
