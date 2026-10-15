"""Incomplete search states for the existing public Toda Narrative entry point.

A partial proof is not a TodaGroupProofPresentation: its unproved goals must
never be promoted to derivations, nor may a completed root be synthesized.
"""
from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import (
    GroupStructureStatus,
    PartialProofResult,
    ProofSearchStatus,
)
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from web_group_proof_common import _group_proof_statement_latex


def _partial_statement_math(statement):
    if isinstance(statement, str):
        return statement
    latex, _fallback = _group_proof_statement_latex(statement)
    if latex is not None:
        return "$" + latex + "$"
    if isinstance(statement, TodaPrimaryGroup):
        return (
            f"$\\pi_{{{statement.group_dimension}}}"
            f"^{{{statement.sphere_dimension}}}$"
        )
    group = getattr(statement, "group", None)
    if isinstance(group, TodaPrimaryGroup):
        return _partial_statement_math(group) + " の群構造の決定"
    return type(statement).__name__ + "（数式表示未対応）"


def render_incomplete_public_narrative(result: PartialProofResult) -> str:
    """Render only verified steps and explicitly label unresolved obligations."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is ProofSearchStatus.COMPLETE:
        raise ValueError("completed search requires TodaGroupProofPresentation")

    status = {
        ProofSearchStatus.PARTIAL: "部分証明・未完成",
        ProofSearchStatus.SEARCH_FAILED: "証明未完成",
        ProofSearchStatus.NOT_SEARCHED: "未探索",
    }[result.status]
    target = _partial_statement_math(result.target)
    if result.open_goals:
        target = _partial_statement_math(result.open_goals[0])
    lines = ["## 証明対象", target, "", f"**探索状態：{status}**"]
    if result.structure_status is GroupStructureStatus.UNKNOWN:
        lines.append("群構造の証明状態: unknown（この探索では未確定）")
    if result.references:
        lines.extend(("", "## 使用する結果（Reference）"))
        for reference in result.references:
            lines.append("- " + reference)

    lines.extend(("", "## 証明（Proof（導出済み））"))
    used = set()
    for step in result.proven_steps:
        if id(step) in used:
            continue
        used.add(id(step))
        if isinstance(step.conclusion, str):
            lines.append(step.conclusion)
        else:
            lines.append(_render_generic_narrative_step(step))
    if not result.proven_steps:
        lines.append("証明できた数学的な ProofStep はまだありません。")

    if result.open_goals:
        lines.extend(("", "## 未解決 Goal"))
        for goal in result.open_goals:
            lines.append("- " + _partial_statement_math(goal))

    if result.diagnostics:
        lines.extend(("", "## 探索診断"))
        for diagnostic in result.diagnostics:
            if diagnostic.startswith("expected one registered derivation for "):
                lines.append("- この目標を導出する型付き Reference と推論規則の組み合わせが見つかりません。")
            elif "SOURCE_ARCHIVE" in diagnostic:
                lines.append("- 数学的に型付けされていない出典テキストは証明に利用していません。")
            else:
                lines.append("- " + diagnostic)

    if result.status is ProofSearchStatus.NOT_SEARCHED:
        lines.extend(("", "証明探索はまだ実行されていません。"))
    else:
        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))
    return "\n".join(lines)
