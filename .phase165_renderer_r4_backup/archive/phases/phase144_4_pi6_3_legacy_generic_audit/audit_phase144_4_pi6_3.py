from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
    render_toda_group_proof_generic_proof_markdown,
)
from toda_group_proof_narrative_blocks import (
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)


@dataclass(frozen=True)
class FeatureAudit:
    name: str
    legacy_patterns: tuple[str, ...]
    generic_patterns: tuple[str, ...]
    semantic_keywords: tuple[str, ...]
    note: str


FEATURES = (
    FeatureAudit(
        name="Definition",
        legacy_patterns=(r"定める", r"\\nu'"),
        generic_patterns=(r"定める|定義", r"\\nu'"),
        semantic_keywords=("DEFINITION",),
        note="ν′ の定義が generic structure / renderer に届いているか。",
    ),
    FeatureAudit(
        name="Toda theorem / lemma references",
        legacy_patterns=(r"\[R[1-9][0-9]*\]", r"Toda"),
        generic_patterns=(r"Toda",),
        semantic_keywords=("REFERENCE", "PRECONDITION"),
        note="定理・補題の provenance が semantic structure にあり、本文に表示されるか。",
    ),
    FeatureAudit(
        name="EHP exact sequence",
        legacy_patterns=(r"完全列", r"\\pi_\{5\}\^\{2\}", r"\\pi_\{6\}\^\{3\}"),
        generic_patterns=(r"完全列", r"\\pi_\{5\}\^\{2\}", r"\\pi_\{6\}\^\{3\}"),
        semantic_keywords=("EXACTNESS",),
        note="EHP 完全列そのものの表示。",
    ),
    FeatureAudit(
        name="Calculation process",
        legacy_patterns=(r"2\\eta_\{3\}", r"2\\nu'", r"\\eta_\{3\}\^\{3\}"),
        generic_patterns=(r"2\\eta_\{3\}", r"2\\nu'", r"\\eta_\{3\}\^\{3\}"),
        semantic_keywords=("CALCULATION",),
        note="2η₃=0, 2ν′=η₃³ などの計算過程。",
    ),
    FeatureAudit(
        name="Order determination",
        legacy_patterns=(r"位数", r"4"),
        generic_patterns=(r"位数|order", r"4"),
        semantic_keywords=("ORDER",),
        note="ν′ の位数 4 の決定。",
    ),
    FeatureAudit(
        name="Short exact sequence",
        legacy_patterns=(
            r"0\\longrightarrow\\pi_\{5\}\^\{2\}",
            r"\\pi_\{6\}\^\{3\}",
            r"\\longrightarrow 0",
        ),
        generic_patterns=(
            r"0\\longrightarrow\s*\\pi_\{5\}\^\{2\}",
            r"\\pi_\{6\}\^\{3\}",
            r"\\longrightarrow 0",
        ),
        semantic_keywords=("EXACTNESS", "MAP_PROPERTY"),
        note="完全性と写像の性質から得る短完全列。",
    ),
    FeatureAudit(
        name="Group structure",
        legacy_patterns=(r"\\pi_\{6\}\^\{3\}", r"\\mathbb\{Z\}/4", r"\\nu'"),
        generic_patterns=(r"\\pi_\{6\}\^\{3\}", r"\\mathbb\{Z\}/4", r"\\nu'"),
        semantic_keywords=("GROUP_STRUCTURE",),
        note="π₆³ = Z/4{ν′} の最終群構造。",
    ),
    FeatureAudit(
        name="Equation numbering and references",
        legacy_patterns=(r"\\tag\{3\}", r"\\tag\{16\}", r"\\tag\{19\}", r"\\tag\{20\}"),
        generic_patterns=(r"\\tag\{",),
        semantic_keywords=(),
        note="式番号の付与と本文からの参照。semantic role から一般化すべき表示機能。",
    ),
    FeatureAudit(
        name="Paragraph flow / connective prose",
        legacy_patterns=(r"まず|次に|さらに|したがって|これらから|このことから",),
        generic_patterns=(r"まず|次に|さらに|したがって|これらから|このことから|より,",),
        semantic_keywords=(),
        note="数学書としての段落構成・接続語。",
    ),
    FeatureAudit(
        name="Final conclusion",
        legacy_patterns=(r"\\pi_\{6\}\^\{3\}", r"\\mathbb\{Z\}/4", r"\\nu'"),
        generic_patterns=(r"\\pi_\{6\}\^\{3\}", r"\\mathbb\{Z\}/4", r"\\nu'"),
        semantic_keywords=("GROUP_STRUCTURE", "TARGET"),
        note="証明の最終結論。",
    ),
)


def _matches_all(text: str, patterns: tuple[str, ...]) -> bool:
    return all(re.search(pattern, text, re.MULTILINE) is not None for pattern in patterns)


def _build_pi6_3():
    report = build_standard_toda_report(n=3, k=3)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(group_result, max_depth=3)
    presentation = build_toda_group_proof_presentation(replay)
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=sidecar,
    )
    return presentation, sidecar, blocks


def _semantic_inventory(presentation, sidecar, blocks) -> str:
    lines = []
    lines.append(f"nodes={len(presentation.nodes)}")
    lines.append(f"blocks={len(blocks)}")
    lines.append("")
    lines.append("BLOCKS")
    lines.append("-" * 78)

    for index, block in enumerate(blocks, start=1):
        role = getattr(block.role, "name", str(block.role))
        lines.append(f"B{index:02d}: role={role} steps={len(block.steps)}")
        for step in block.steps:
            conclusion = step.conclusion
            rule = (
                step.inference_rule.name
                if step.inference_rule is not None
                else "-"
            )
            lines.append(
                "  "
                + type(conclusion).__name__
                + " | rule="
                + rule
            )

    lines.append("")
    lines.append("SEMANTIC SIDECAR")
    lines.append("-" * 78)
    lines.append(repr(sidecar))
    lines.append("")
    return "\n".join(lines)


def _semantic_has(inventory: str, keywords: tuple[str, ...]) -> bool:
    if not keywords:
        return False
    upper = inventory.upper()
    return any(keyword.upper() in upper for keyword in keywords)


def _classify(
    feature: FeatureAudit,
    legacy: str,
    generic: str,
    inventory: str,
) -> tuple[str, str]:
    legacy_has = _matches_all(legacy, feature.legacy_patterns)
    generic_has = _matches_all(generic, feature.generic_patterns)
    semantic_has = _semantic_has(inventory, feature.semantic_keywords)

    if generic_has:
        return (
            "A",
            "generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。",
        )

    if legacy_has and semantic_has:
        return (
            "B",
            "legacy には表示され、generic semantic structure に関連情報もある。generic renderer 側の残存不足候補。",
        )

    if legacy_has and not semantic_has:
        if feature.name in {
            "Equation numbering and references",
            "Paragraph flow / connective prose",
        }:
            return (
                "B",
                "legacy の presentation 機能。数学的事実の欠落ではなく generic renderer の一般表示規則として検討する。",
            )
        return (
            "D",
            "legacy にはあるが generic structure から必要情報を確認できない。Semantic / Argument への到達経路を調査する。",
        )

    if not legacy_has and not generic_has:
        return (
            "C",
            "今回の legacy π₆³ の基準出力にも generic 出力にも確認できない。旧 renderer 固有機能として本当に必要か再確認する。",
        )

    return (
        "A",
        "generic に存在する。legacy との差は機能欠落ではない。",
    )


def main() -> int:
    presentation, sidecar, blocks = _build_pi6_3()

    legacy = render_toda_group_proof_narrative_markdown(presentation)
    generic = render_toda_group_proof_generic_proof_markdown(
        presentation,
        blocks,
    )
    inventory = _semantic_inventory(presentation, sidecar, blocks)

    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "legacy_pi6_3.md").write_text(legacy, encoding="utf-8")
    (out_dir / "generic_pi6_3.md").write_text(generic, encoding="utf-8")
    (out_dir / "semantic_inventory.txt").write_text(
        inventory,
        encoding="utf-8",
    )

    rows = []
    for feature in FEATURES:
        classification, reason = _classify(
            feature,
            legacy,
            generic,
            inventory,
        )
        rows.append((feature, classification, reason))

    report_lines = [
        "# Phase 144-4 π₆³ legacy vs generic 残存差分監査",
        "",
        "## 目的",
        "",
        "Phase 139〜143 で構築した generic Narrative engine を作り直さず、",
        "現在の legacy π₆³ Narrative と generic π₆³ proof text の差を機能単位で分類する。",
        "",
        "分類:",
        "",
        "- A: Phase 143 までに一般化済み。generic で表示可能。",
        "- B: generic renderer の表示規則に残存不足がある。",
        "- C: legacy にしかないが、不要または基準出力にも確認できない。",
        "- D: 数学的情報が generic Semantic / Argument structure に届いていない疑い。",
        "",
        "## 実行概要",
        "",
        f"- presentation nodes: {len(presentation.nodes)}",
        f"- narrative blocks: {len(blocks)}",
        f"- legacy chars: {len(legacy)}",
        f"- generic chars: {len(generic)}",
        "",
        "## 分類結果",
        "",
        "| 機能 | 分類 | 判定理由 |",
        "|---|---|---|",
    ]

    for feature, classification, reason in rows:
        report_lines.append(
            f"| {feature.name} | **{classification}** | {reason} |"
        )

    report_lines.extend(
        [
            "",
            "## 各監査項目",
            "",
        ]
    )

    for feature, classification, reason in rows:
        report_lines.extend(
            [
                f"### {feature.name}",
                "",
                f"- 分類: **{classification}**",
                f"- 観点: {feature.note}",
                f"- 判定: {reason}",
                "",
            ]
        )

    report_lines.extend(
        [
            "## Phase 144-5 への入力",
            "",
            "Phase 144-5 では、この監査で **B / D** に分類された項目だけを修正対象候補とする。",
            "A は再実装しない。C は必要性を確認するまで実装しない。",
            "",
            "特に、群座標 `n == 3 and k == 3` による本番 renderer の追加分岐は禁止する。",
            "",
        ]
    )

    report = "\n".join(report_lines)
    (out_dir / "phase144_4_audit_report.md").write_text(
        report,
        encoding="utf-8",
    )

    print("=" * 78)
    print("Phase 144-4 pi_6^3 legacy vs generic residual-difference audit")
    print("=" * 78)
    print(f"nodes={len(presentation.nodes)}")
    print(f"blocks={len(blocks)}")
    print(f"legacy_chars={len(legacy)}")
    print(f"generic_chars={len(generic)}")
    print()
    for feature, classification, reason in rows:
        print(f"[{classification}] {feature.name}")
        print(f"    {reason}")
    print()
    print("Generated:")
    print("  output/legacy_pi6_3.md")
    print("  output/generic_pi6_3.md")
    print("  output/semantic_inventory.txt")
    print("  output/phase144_4_audit_report.md")
    print()
    print("AUDIT ONLY: no production source files were modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
