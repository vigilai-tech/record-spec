"""record CLI — validate and gap-analyze RECORD trace documents."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from record_py.gap_analyzer import GapAnalyzer, KNOWN_REGULATIONS
from record_py.validator import RecordValidator


# ── formatting helpers ────────────────────────────────────────────────────────

_BAR = "═" * 44  # ════…


def _header(title: str) -> None:
    print(f"\n{title}")
    print(_BAR)


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)


# ── commands ──────────────────────────────────────────────────────────────────

def _cmd_validate(args: argparse.Namespace) -> None:
    path = Path(args.file)
    doc = _load_json(path)

    validator = RecordValidator()
    result = validator.validate(doc)

    _header("RECORD Schema Validation")
    print(f"File:    {path.name}")

    if result["valid"]:
        print("Result:  PASS\n")
        print("All required fields present and valid.")
    else:
        print("Result:  FAIL\n")
        for err in result["errors"]:
            print(f"  • {err}")
        sys.exit(1)


def _cmd_gap_analyze(args: argparse.Namespace) -> None:
    path = Path(args.file)
    doc = _load_json(path)

    try:
        analyzer = GapAnalyzer(args.regulation)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    report = analyzer.analyze(doc)

    _header(f"RECORD Gap Analysis — {report['regulation_name']}")
    print(f"File:        {path.name}")
    print(f"Regulation:  {report['regulation']}\n")

    score_int = int(report["score"])
    print(f"Compliance Score:  {score_int}%  {report['status']}\n")

    # Required fields
    req = report["required"]
    req_present = sum(1 for r in req if r["present"])
    print(f"Required Fields ({req_present}/{len(req)})")
    for r in req:
        mark = "✓" if r["present"] else "✗"
        field_col = f"  {mark}  {r['field']:<30}"
        print(f"{field_col} {r['article']}")
        if not r["present"]:
            print(f"       {r['reason']}")

    # Recommended fields
    rec = report["recommended"]
    if rec:
        rec_present = sum(1 for r in rec if r["present"])
        print(f"\nRecommended Fields ({rec_present}/{len(rec)})")
        for r in rec:
            mark = "✓" if r["present"] else "✗"
            field_col = f"  {mark}  {r['field']:<30}"
            print(f"{field_col} {r['article']}")
            if not r["present"]:
                print(f"       {r['reason']}")

    print()


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="record",
        description="RECORD — validate traces and analyze regulatory compliance gaps.",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # validate
    val = sub.add_parser("validate", help="Validate a trace against the RECORD schema")
    val.add_argument("file", help="Path to a RECORD JSON file")

    # gap-analyze
    gap = sub.add_parser("gap-analyze", help="Score a trace against a regulation's field requirements")
    gap.add_argument("file", help="Path to a RECORD JSON file")
    gap.add_argument(
        "--regulation",
        required=True,
        metavar="ID",
        help=f"Regulation ID. One of: {', '.join(KNOWN_REGULATIONS)}",
    )

    args = parser.parse_args()

    if args.command == "validate":
        _cmd_validate(args)
    elif args.command == "gap-analyze":
        _cmd_gap_analyze(args)
    else:
        parser.print_help()
        sys.exit(1)
