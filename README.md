# RECORD — Regulatory Evidence Capture of Reasoning and Decisions

![Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Version](https://img.shields.io/badge/version-v0.1-green.svg)
![OpenInference Extension](https://img.shields.io/badge/OpenInference-extension-orange.svg)

RECORD is an open standard that extends the [OpenInference](https://github.com/Arize-ai/openinference) observability specification with fields specifically required for regulatory compliance in financial AI agents. Where OpenInference captures *what* an LLM-based system did (spans, tokens, latency, retrieval), RECORD captures *why* a decision was made, *which rules* were evaluated, *what data* was present at the moment of decision, and *what a human did* with the agent's recommendation — the four dimensions that financial regulators consistently demand during examinations, model-risk reviews, and enforcement proceedings. RECORD traces are designed to be emitted as a single JSON document alongside or within an existing OpenTelemetry/OpenInference span, with no changes required to your existing observability pipeline.

The schema covers every layer of a financial AI agent's audit trail: regulatory authority linkage (`authority_basis`), operating-mode declaration (`operating_domain`), feature-level explainability (`influencing_parameters`), policy-rule evaluation logs (`policy_evaluation`), full chain-of-thought capture, tool-call inventories, data-source provenance hashes, human-disposition records, and downstream outcome linkage. Each field is tagged as **required**, **recommended**, or **optional** and is mapped in [REGULATORY_MAPPING.md](./REGULATORY_MAPPING.md) to the specific article or section of EU AI Act, MiFID II RTS 6, FinCEN AML NPRM 2026, SR 11-7, ECOA Regulation B §202.9, or SOX §302 that motivates its capture. This means compliance teams can use RECORD traces directly as primary evidence in regulatory submissions, model-risk governance packages, or SAR documentation without reformatting or post-hoc reconstruction.

RECORD v0.1 is a community draft and welcomes contributions under the Apache 2.0 license. Three reference examples are included in the [examples/](./examples/) directory: a MiFID II trade-surveillance layering alert triaged by an L1 agent and escalated to L2 ([trade_surveillance_l1.json](./examples/trade_surveillance_l1.json)), a FinCEN AML wire-transfer triage with SAR narrative generation ([aml_triage.json](./examples/aml_triage.json)), and a MAR Art. 14 communication-surveillance case where an agent detects insider tipping via bookkeeping cross-reference of deal-room access logs, Bloomberg chat content, and counterparty options flow ([communication_surveillance_l1.json](./examples/communication_surveillance_l1.json)). All examples are valid against [schema.json](./schema.json) and are intended to serve as integration templates for teams building compliant AI agents in trading surveillance, financial crime, and communication monitoring domains.

## Quick Start

```bash
# Validate a RECORD document against the schema
npx ajv-cli validate -s schema.json -d examples/trade_surveillance_l1.json

# Python
pip install jsonschema
python -c "
import json, jsonschema
schema = json.load(open('schema.json'))
doc    = json.load(open('examples/aml_triage.json'))
jsonschema.validate(doc, schema)
print('valid')
"
```

## Repository Structure

```
record-spec/
├── schema.json               # Canonical JSON Schema (draft-07)
├── REGULATORY_MAPPING.md     # Field → regulation cross-reference
├── LICENSE                   # Apache 2.0
└── examples/
    ├── trade_surveillance_l1.json         # MiFID II layering alert, L1→L2 escalation
    ├── aml_triage.json                    # AML wire-transfer triage + SAR draft
    └── communication_surveillance_l1.json # MAR Art.14 insider tipping, direct legal escalation
```

## Field Requirement Levels

| Level | Meaning |
|---|---|
| **REQUIRED** | Must be present in every RECORD document. Validators will reject documents missing these fields. |
| **RECOMMENDED** | Should be present for the domain indicated by `authority_basis`. Omission must be justified. |
| **OPTIONAL** | Present when available; aids correlation and reproducibility but not mandatory. |

## Contributing

Open an issue or pull request at [record-spec/record-spec](https://github.com/record-spec/record-spec). Please include a regulatory citation when proposing new fields.
