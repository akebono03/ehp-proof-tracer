"""Validated, proof-step-indexed narrative body projection.

This module never infers citations from mathematical text or rule names.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex


@dataclass(frozen=True)
class NarrativeBodyLine:
    step_index: int
    statement_latex: str
    citation_numbers: tuple[int, ...]
    role: str


def build_narrative_body_lines(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> tuple[NarrativeBodyLine, ...]:
    """Bind renderable conclusions to their exact Proof Tree citation indices.

    Unrenderable conclusions are not replaced with guessed prose. Citation
    membership is validated in both directions; a malformed model fails closed.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if model.steps != result.proven_steps:
        raise ValueError("model steps must match the searched result")
    if len(model.step_citation_numbers) != len(model.steps):
        raise ValueError("step citation mapping has the wrong length")
    if result.status is ProofSearchStatus.COMPLETE and model.root_index is None:
        raise ValueError("complete result requires a root step")
    if model.root_index is not None and not 0 <= model.root_index < len(model.steps):
        raise ValueError("root step index is invalid")

    known = {citation.number: citation for citation in model.citations}
    if len(known) != len(model.citations) or set(known) != set(range(1, len(known) + 1)):
        raise ValueError("citation numbers must be unique and contiguous")
    for number, citation in known.items():
        for index in citation.step_indices:
            if not 0 <= index < len(model.steps):
                raise ValueError("citation refers to a nonexistent proof step")
            if number not in model.step_citation_numbers[index]:
                raise ValueError("citation and step map disagree")

    lines = []
    for index, step in enumerate(model.steps):
        numbers = model.step_citation_numbers[index]
        if len(set(numbers)) != len(numbers):
            raise ValueError("a proof step contains duplicate citation numbers")
        for number in numbers:
            if number not in known or index not in known[number].step_indices:
                raise ValueError("step cites a missing or unrelated source")
        latex, fallback_type = _group_proof_statement_latex(step.conclusion)
        if latex is None or fallback_type is not None:
            continue
        role = "given" if step.rule is ProofRule.GIVEN else (
            "root" if index == model.root_index else "inference"
        )
        lines.append(NarrativeBodyLine(index, latex, numbers, role))
    return tuple(lines)
