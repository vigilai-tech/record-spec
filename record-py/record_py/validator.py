"""RecordValidator — validates RECORD dicts against the canonical schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft7Validator


class RecordValidator:
    """Validates RECORD documents against a JSON Schema file.

    Args:
        schema_path: Path to ``schema.json``. Defaults to the repo-root
            ``schema.json`` when the package is used in-tree.
    """

    def __init__(self, schema_path: str | Path | None = None) -> None:
        if schema_path is None:
            schema_path = Path(__file__).parent.parent.parent / "schema.json"
        self.schema_path = Path(schema_path)
        if not self.schema_path.exists():
            raise FileNotFoundError(
                f"schema.json not found at {self.schema_path}. "
                "Pass schema_path= explicitly."
            )
        self.schema: dict = json.loads(self.schema_path.read_text(encoding="utf-8"))
        self._validator = Draft7Validator(self.schema)

    def validate(self, doc: dict[str, Any]) -> dict[str, Any]:
        """Return ``{"valid": bool, "errors": [str, ...]}`` for *doc*."""
        errors = [
            f"{'.'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
            for e in sorted(self._validator.iter_errors(doc), key=str)
        ]
        return {"valid": not errors, "errors": errors}
