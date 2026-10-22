"""Dependency-aware narrative projection from already proven ProofSteps.

No new theorem, source, or mathematical identity is inferred here.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_13_dependency_model import build_narrative_inferences
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex


@dataclass(frozen=True)
class NarrativeReasonedLine:
    step_index: int
    premise_indices: tuple[int, ...]
    conclusion_latex: str | None
    premise_latex: tuple[str, ...]
    citation_numbers: tuple[int, ...]
    role: str


def build_reasoned_narrative_lines(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> tuple[NarrativeReasonedLine, ...]:
    """Project explicit dependencies into sentences without guessing reasons."""
    inferences = build_narrative_inferences(result, model)
    lines = []
    for item in inferences:
        if item.unresolved_premises:
            raise ValueError("unresolved premise: narrative cannot assert a derivation")
        step = model.steps[item.step_index]
        latex, fallback = _group_proof_statement_latex(step.conclusion)
        if fallback is not None:
            latex = None
        premise_latex = []
        for ancestor in item.premise_indices:
            premise, ancestor_fallback = _group_proof_statement_latex(
                model.steps[ancestor].conclusion
            )
            if premise is not None and ancestor_fallback is None:
                premise_latex.append(premise)
        role = ("given" if step.rule is ProofRule.GIVEN else
                "root" if item.is_root else "inference")
        lines.append(NarrativeReasonedLine(
            step_index=item.step_index,
            premise_indices=item.premise_indices,
            conclusion_latex=latex,
            premise_latex=tuple(premise_latex),
            citation_numbers=item.citation_numbers,
            role=role,
        ))
    return tuple(lines)


def render_reasoned_narrative_markdown(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> str:
    """Render a verbose opt-in evidence trace with explicit premise links.

    This is not yet the final mathematical prose generator: unrenderable
    statements are identified by step number, never turned into guessed math.
    """
    lines = build_reasoned_narrative_lines(result, model)
    output = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        output.extend((f"**[R{citation.number}] {locator}.**", ""))
    output.extend(("証明", ""))
    for line in lines:
        index = line.step_index + 1
        tags = ", ".join(f"[R{number}]" for number in line.citation_numbers)
        if line.role == "given":
            opening = f"{tags}より" if tags else "既知の命題として"
        elif line.premise_indices:
            refs = ", ".join(f"ステップ{item + 1}" for item in line.premise_indices)
            opening = f"{refs}を前提として"
            if tags:
                opening += f"、{tags}を用いて"
        else:
            opening = f"{tags}を用いて" if tags else "証明済みの推論により"
        if line.conclusion_latex is None:
            sentence = f"ステップ{index}：{opening}、型付き命題を導く（数式表示未対応）。"
        else:
            sentence = f"ステップ{index}：{opening}、${line.conclusion_latex}$ を得る。"
        output.extend((sentence, ""))
    if result.status is ProofSearchStatus.COMPLETE:
        output.append("□")
    return "\n".join(output).rstrip() + "\n"
