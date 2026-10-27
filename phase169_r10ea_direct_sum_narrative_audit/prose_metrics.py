"""Pure, read-only metrics for text rendered from an already-verified proof."""
from __future__ import annotations

import re
from collections import Counter

IMAGE_FORMULA = re.compile(r"\$E\(([^$\n]+)\)=([^$\n]+)\$")

def count_rendered_image_equations(markdown: str) -> dict:
    """Count exact displayed one-step E equalities, not hypothetical proof steps.

    Match the mathematics inside a dollar-delimited formula; differing citation
    prefixes do not make repeated occurrences distinct. No prose is suppressed.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")
    occurrences = Counter(
        (match.group(1), match.group(2))
        for match in IMAGE_FORMULA.finditer(markdown)
    )
    repeated = [
        {"from": source, "to": target, "copies": copies}
        for (source, target), copies in occurrences.items()
        if copies > 1
    ]
    return {
        "total_occurrences": sum(occurrences.values()),
        "distinct_equations": len(occurrences),
        "extra_duplicate_occurrences": sum(x["copies"] - 1 for x in repeated),
        "repeated_equations": repeated,
    }


def render_report(report: dict) -> str:
    """Summarize only measured output; do not invent or normalize proof facts."""
    lines = [
        "# Phase 169 R10EA — 直和群の証明文章監査",
        "",
        "AUDIT_ONLY: 本番コード・既存テスト・Proof Tree は変更しない。",
        "",
        "| 群 | 探索 | Trust Boundary | INFERENCE の生成元像 | 元の数式表示未対応 | 表示された E 等式 | 重複表示 | 本文文字数 |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for case in report["cases"]:
        rendered = case.get("rendered_image_equations", {})
        lines.append(
            f"| `{case['goal']}` | {case['search_status']} | "
            f"{case['trust_boundary']} | {case['inferred_generator_image_steps']} | "
            f"{case.get('images_without_supported_element_tex', '—')} | "
            f"{rendered.get('total_occurrences', '—')} | "
            f"{rendered.get('extra_duplicate_occurrences', '—')} | "
            f"{case.get('rendered_characters', '—')} |"
        )
    for case in report["cases"]:
        lines.extend(("", f"## {case['goal']}", ""))
        lines.append(f"- 検証結果: {case['trust_boundary']}")
        if case.get("trust_error"):
            lines.append(f"- 拒否理由: `{case['trust_error']}`")
        if case.get("open_goal_types"):
            lines.append("- 未解決型: " + ", ".join(case["open_goal_types"]))
        for duplicate in case.get("rendered_image_equations", {}).get("repeated_equations", [])[:12]:
            lines.append(
                f"- 重複表示 {duplicate['copies']}回: "
                f"$E({duplicate['from']})={duplicate['to']}$"
            )
        if case.get("rendered_file"):
            lines.append("- 証明文章の原本: `output/" + case["rendered_file"] + "`")
    lines.extend((
        "", "## 次の実装との境界", "",
        "重複・冗長さの削減は、検証済み ProofStep と引用番号を変更せず、",
        "Narrative Projection（文章投影）の表示だけで行う。",
        "本監査は証明生成や群構造の修正を提案しない。",
        "全体 pytest は Phase 169 の終了時に実施する。",
        "",
    ))
    return "\n".join(lines)

