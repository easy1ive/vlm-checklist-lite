#!/usr/bin/env python3
"""Run a demo evaluation and save JSON report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vlm_checklist_lite.evaluator import CapabilityEvaluator


def main() -> None:
    parser = argparse.ArgumentParser(description="Run checklist-lite evaluation")
    parser.add_argument("--input", default="examples/dev_split.jsonl", help="Input JSONL path")
    parser.add_argument("--output", default="outputs/report.json", help="Output JSON report path")
    args = parser.parse_args()

    evaluator = CapabilityEvaluator()
    report = evaluator.evaluate_jsonl(args.input)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
