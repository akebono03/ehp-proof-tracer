"""Shared typed-proof Narrative used when a legacy transport display would misstate ancestry.

This is an internal presentation helper; the one public entry remains
render_toda_group_proof_narrative_markdown. No theorem or premise is invented.
"""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofRule, ProofStep
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from web_group_proof_common import _group_proof_statement_latex


def ordered_proof_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    """Return deduplicated ancestors before dependents, including the root."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be ProofStep")
    seen: set[int] = set()
    active: set[int] = set()
    ordered: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("every proof premise must be ProofStep")
        key = id(step)
        if key in active:
            raise ValueError("cyclic ProofStep ancestry")
        if key in seen:
            return
        active.add(key)
        for premise in step.premises:
            visit(premise)
        active.remove(key)
        seen.add(key)
        ordered.append(step)

    visit(root)
    return tuple(ordered)


def has_transport_proof_ancestry(root: ProofStep) -> bool:
    """Inspect proved inferences, never infer transport from a group number."""
    return any(
        step.rule is ProofRule.INFERENCE
        and (
            "transport" in str(getattr(step.inference_rule, "name", "")).lower()
            or "4.5" in str(getattr(step.inference_rule, "name", ""))
        )
        for step in ordered_proof_ancestry(root)
    )


def _math_statement(statement: object) -> str:
    latex, _fallback = _group_proof_statement_latex(statement)
    if latex is None:
        raise ValueError("typed mathematical statement cannot be rendered")
    return "$" + latex + "$"


def _reference_label(step: ProofStep) -> str:
    metadata = getattr(step.inference_rule, "literature_reference", None)
    locator = getattr(metadata, "locator", None) or getattr(metadata, "label", None)
    if locator:
        return str(locator)
    name = str(getattr(step.inference_rule, "name", ""))
    if name.startswith("Adopted literature "):
        return name.removeprefix("Adopted literature ")
    raise ValueError("GIVEN ProofStep has no source locator; refuse citation-free narrative")


def render_completed_from_proofsteps(result: PartialProofResult, root: ProofStep) -> str:
    """Render facts, citations, and rules from actual completed ProofSteps only."""
    if not isinstance(result, PartialProofResult) or result.status is not ProofSearchStatus.COMPLETE:
        raise ValueError("complete typed proof result required")
    if root.conclusion != result.conclusion or root.rule is not ProofRule.INFERENCE:
        raise ValueError("root must prove the completed conclusion")
    ancestry = ordered_proof_ancestry(root)
    leaves = tuple(step for step in ancestry if step.rule is ProofRule.GIVEN)
    inferences = tuple(step for step in ancestry if step.rule is ProofRule.INFERENCE)
    if not leaves or not inferences:
        raise ValueError("completed proof must contain cited leaves and inference")
    citations: dict[int, str] = {}
    reference_rows: list[str] = []
    for step in leaves:
        label = _reference_label(step)
        number = len(reference_rows) + 1
        citations[id(step)] = f"[R{number}]"
        reference_rows.append(f"**[R{number}] {label}.**")
        reference_rows.append(_render_generic_narrative_step(step))
        reference_rows.append("")

    lines = [
        "## 証明対象", "", _math_statement(root.conclusion), "",
        "## 使用する結果", "", *reference_rows, "---", "", "## 証明", "",
    ]
    for step in inferences:
        rule = getattr(step.inference_rule, "name", None)
        if not rule:
            raise ValueError("inference ProofStep lacks a named inference rule")
        parents = [citations[id(p)] for p in step.premises if id(p) in citations]
        prefix = "、".join(dict.fromkeys(parents)) + "に基づき、" if parents else "前段の導出を用い、"
        if step is root:
            lines.append(f"{prefix}{rule} を適用する。")
        else:
            lines.append(f"{prefix}{rule} により、{_render_generic_narrative_step(step)}")
        lines.append("")
    lines.append("以上より, " + _math_statement(root.conclusion) + ". □")
    return "\n".join(lines)
