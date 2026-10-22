"""Proof-step dependency projection for the shared narrative pipeline.

This is a structural model, not a new mathematical proof generator.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class NarrativeInference:
    step_index: int
    premise_indices: tuple[int, ...]
    unresolved_premises: tuple[object, ...]
    citation_numbers: tuple[int, ...]
    rule: ProofRule
    is_root: bool


def build_narrative_inferences(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> tuple[NarrativeInference, ...]:
    """Index each inference against proven antecedents without inventing edges.

    ``ProofStep.premises`` may contain statements or ProofStep instances.
    Only exact, earlier unique conclusions count as available premises.
    Ambiguous, absent, or forward dependencies are preserved as unresolved.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if model.steps != result.proven_steps:
        raise ValueError("model steps must match the searched result")
    if len(model.step_citation_numbers) != len(model.steps):
        raise ValueError("step citation map length mismatch")
    known = {citation.number: citation for citation in model.citations}
    if len(known) != len(model.citations):
        raise ValueError("duplicate citation numbers")
    nodes = []
    for index, step in enumerate(model.steps):
        indices = []
        unresolved = []
        for premise in step.premises:
            statement = premise.conclusion if isinstance(premise, ProofStep) else premise
            matches = [
                j for j, earlier in enumerate(model.steps[:index])
                if earlier.conclusion == statement
            ]
            if len(matches) != 1:
                unresolved.append(statement)
            else:
                indices.append(matches[0])
        numbers = model.step_citation_numbers[index]
        if any(
            number not in known or index not in known[number].step_indices
            for number in numbers
        ):
            raise ValueError("step cites a missing or unrelated source")
        nodes.append(NarrativeInference(
            step_index=index,
            premise_indices=tuple(indices),
            unresolved_premises=tuple(unresolved),
            citation_numbers=numbers,
            rule=step.rule,
            is_root=index == model.root_index,
        ))
    return tuple(nodes)
