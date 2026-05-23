# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

RECORD (Regulatory Evidence Capture of Reasoning and Decisions) is an open standard — a JSON Schema extension to OpenInference — for audit trails in financial AI agents. The schema captures why a decision was made, which regulatory rules were evaluated, what data was present at decision time, and what a human did with the agent's recommendation.

The repo has two main artifacts:
1. **`schema.json`** — the canonical JSON Schema (draft-07), the single source of truth for what a valid RECORD document looks like.
2. **`record-py/`** — a Python SDK for emitting and validating RECORD traces.

## Validation Commands

```bash
# Validate an example against the schema (Node.js)
npx ajv-cli validate -s schema.json -d examples/trade_surveillance_l1.json

# Validate using Python
python -c "
import json, jsonschema
schema = json.load(open('schema.json'))
doc = json.load(open('examples/aml_triage.json'))
jsonschema.validate(doc, schema)
print('valid')
"
```

## Python SDK

```bash
cd record-py
pip install -e ".[dev]"   # install with dev deps (pytest)
pytest                     # run tests
```

The SDK has three modules:

- **`record_py/emitter.py` — `RecordEmitter`**: Instantiated once per agent with static metadata (`agent_id`, `agent_version`, `authority_basis`, `operating_domain`). Call `.emit()` per decision; it auto-generates `record_id` and `timestamp`, writes a JSONL line to `output_path`, and returns the doc dict.

- **`record_py/validator.py` — `RecordValidator`**: Wraps `jsonschema.Draft7Validator` against `schema.json`. `.validate(doc)` returns `{"valid": bool, "errors": [str]}`. Defaults to the repo-root `schema.json` when used in-tree.

- **`record_py/openinference_adapter.py` — `adapt_span()`**: Converts an OpenInference span dict into a RECORD dict. Required fields not derivable from the span (`authority_basis`, `agent_id`, etc.) must be supplied via `metadata.*` attributes on the span or merged in by the caller.

## Schema Conventions

- All `authority_basis` strings use dot-notation: `<framework>.<article_or_section>` (e.g., `eu_ai_act.art_86`, `mifid2.rts6`, `fincen_aml_nprm_2026.s_1010`).
- `operating_domain` must be one of `autonomous`, `supervised`, or `human_only`.
- `additionalProperties: false` is set at every object level — unknown fields are rejected.
- Fields are tagged `[REQUIRED]`, `[RECOMMENDED]`, or `[OPTIONAL]` in their `description`. Required fields: `record_id`, `timestamp`, `agent_id`, `agent_version`, `authority_basis`, `operating_domain`, `prompt`, `final_action`.

## Regulatory Mapping

`REGULATORY_MAPPING.md` is the cross-reference between schema fields and specific regulatory articles (EU AI Act, MiFID II RTS 6, FinCEN AML NPRM 2026, SR 11-7, ECOA Reg B, SOX §302). When adding or changing fields, update this file with a regulatory citation. Do not add fields without one.

## Examples

The three examples in `examples/` (`trade_surveillance_l1.json`, `aml_triage.json`, `credit_limit_increase.json`) are intended as integration templates and must remain valid against `schema.json`. Always re-validate examples after schema changes.
