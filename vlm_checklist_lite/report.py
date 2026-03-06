"""Report helpers for checklist-lite results."""

from __future__ import annotations

from pathlib import Path
from typing import Dict


def write_markdown_report(report: Dict[str, object], output_path: str | Path) -> None:
    overall = report["overall"]
    per_capability = report["per_capability"]

    lines = [
        "# VLM Checklist Lite Report",
        "",
        "## Overall",
        "",
        f"- Samples: {overall['count']}",
        f"- Exact Match: {overall['exact_match']}",
        f"- Token F1: {overall['token_f1']}",
        "",
        "## Capability Breakdown",
        "",
        "| Capability | Count | Exact Match | Token F1 |",
        "|---|---:|---:|---:|",
    ]

    for capability, stats in per_capability.items():
        lines.append(
            f"| {capability} | {stats['count']} | {stats['exact_match']} | {stats['token_f1']} |"
        )

    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def maybe_plot_radar(report: Dict[str, object], output_path: str | Path) -> bool:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return False

    capabilities = list(report["per_capability"].keys())
    scores = [report["per_capability"][cap]["token_f1"] for cap in capabilities]

    if not capabilities:
        return False

    # Duplicate first point to close the radar polygon.
    values = scores + [scores[0]]
    angles = [n / float(len(capabilities)) * 2 * 3.141592653589793 for n in range(len(capabilities))]
    angles += [angles[0]]

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(capabilities)
    ax.set_ylim(0, 1.0)
    ax.set_title("Token F1 by Capability")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return True
