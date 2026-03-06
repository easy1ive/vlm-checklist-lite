"""Capability-level evaluator and report generator."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List

from .metrics import exact_match, token_f1


@dataclass
class CapabilitySummary:
    count: int
    exact_match: float
    token_f1: float


class CapabilityEvaluator:
    """Aggregate VLM predictions by capability buckets."""

    def load_jsonl(self, path: str | Path) -> List[dict]:
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    def evaluate_records(self, records: List[dict]) -> Dict[str, object]:
        exact_scores: List[float] = []
        f1_scores: List[float] = []

        per_capability_exact: Dict[str, List[float]] = defaultdict(list)
        per_capability_f1: Dict[str, List[float]] = defaultdict(list)

        for r in records:
            pred = r["prediction"]
            ref = r["reference"]
            capability = r["capability"]

            em = exact_match(pred, ref)
            f1 = token_f1(pred, ref)

            exact_scores.append(em)
            f1_scores.append(f1)
            per_capability_exact[capability].append(em)
            per_capability_f1[capability].append(f1)

        per_capability: Dict[str, CapabilitySummary] = {}
        for cap in sorted(per_capability_exact):
            cap_exact = per_capability_exact[cap]
            cap_f1 = per_capability_f1[cap]
            per_capability[cap] = CapabilitySummary(
                count=len(cap_exact),
                exact_match=round(sum(cap_exact) / len(cap_exact), 4),
                token_f1=round(sum(cap_f1) / len(cap_f1), 4),
            )

        result = {
            "overall": {
                "count": len(records),
                "exact_match": round(sum(exact_scores) / len(exact_scores), 4) if exact_scores else 0.0,
                "token_f1": round(sum(f1_scores) / len(f1_scores), 4) if f1_scores else 0.0,
            },
            "per_capability": {
                cap: {
                    "count": summary.count,
                    "exact_match": summary.exact_match,
                    "token_f1": summary.token_f1,
                }
                for cap, summary in per_capability.items()
            },
        }
        return result

    def evaluate_jsonl(self, path: str | Path) -> Dict[str, object]:
        return self.evaluate_records(self.load_jsonl(path))
