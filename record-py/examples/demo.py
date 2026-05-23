"""demo.py — emit one communication-surveillance RECORD trace, then validate all four examples."""

import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from record_py import RecordEmitter, RecordValidator

ROOT = Path(__file__).parent.parent.parent
schema_path = ROOT / "schema.json"

# Emit a minimal communication-surveillance trace
emitter = RecordEmitter(
    agent_id="comms-surveillance-l1-agent", agent_version="4.0.2",
    authority_basis=["eu_mar.art_14", "eu_mar.art_16", "finra.rule_3110"],
    operating_domain="supervised", output_path="/tmp/record_demo.jsonl",
)
doc = emitter.emit(
    prompt="Evaluate flagged Bloomberg IB chat COMMS-2026-DEMO-001. Sender is on IB deal team for NVDA. NLP score 0.94.",
    final_action={"type": "escalate_legal", "disposition": "MAR Art.14 tipping elements satisfied. Escalating to Legal.", "severity_score": 9.1, "escalated": True},
    influencing_parameters=[{"factor": "mnpi_keyword_score", "value": 0.94, "weight": 0.31}, {"factor": "counterparty_trade_latency_minutes", "value": 32, "weight": 0.21}],
    policy_evaluation=[{"rule_id": "MAR-P1-MNPI-KEYWORD", "rule_name": "MNPI Keyword Detection", "verdict": "fail", "confidence": 0.94}, {"rule_id": "MAR-P2-INFO-BARRIER", "rule_name": "Information Barrier Integrity", "verdict": "fail", "confidence": 0.97}],
    chain_of_thought=[{"step": 1, "content": "Chat contains 'you didn't hear it from me' — canonical tipping indicator.", "type": "observation"}, {"step": 2, "content": "Sender exited IB deal room 22 min before sending chat. MAR Art.14(3) elements satisfied.", "type": "conclusion"}],
)

# Validate the emitted trace + all four repo examples
validator = RecordValidator(schema_path)
targets = {"[emitted]": doc, **{p.name: json.loads(p.read_text()) for p in sorted((ROOT / "examples").glob("*.json"))}}

print(f"{'File':<45} Result")
print("-" * 52)
all_pass = True
for name, record in targets.items():
    result = validator.validate(record)
    print(f"{name:<45} {'PASS' if result['valid'] else 'FAIL'}")
    for err in result["errors"]:
        print(f"  {'':43} {err}")
    if not result["valid"]:
        all_pass = False

print()
print("All records valid." if all_pass else "One or more records failed.")
sys.exit(0 if all_pass else 1)
