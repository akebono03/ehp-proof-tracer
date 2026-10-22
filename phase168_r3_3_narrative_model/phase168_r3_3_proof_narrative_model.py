"""Proof-tree-backed citation projection; no rendering or search decisions."""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult
from proof import LiteratureReference, ProofStep
from unified_statement_registry import ProofStepLink, UnifiedStatementRegistry


@dataclass(frozen=True)
class NarrativeCitation:
    number: int
    reference: LiteratureReference
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProofNarrativeModel:
    steps: tuple[ProofStep, ...]
    citations: tuple[NarrativeCitation, ...]
    step_citation_numbers: tuple[tuple[int, ...], ...]
    root_index: int | None


def build_proof_narrative_model(
    result: PartialProofResult,
    *,
    registry: UnifiedStatementRegistry | None = None,
    proof_links: tuple[ProofStepLink, ...] = (),
) -> ProofNarrativeModel:
    """Project only explicit proof-step and registered-link citations.

    Matching a link requires an exact ProofStep value; merely matching a
    conclusion or a display string is not sufficient. Root inference citations
    remain eligible. Neither a root conclusion nor an unused registry assertion
    becomes a premise through this projection.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if registry is not None and not isinstance(registry, UnifiedStatementRegistry):
        raise TypeError("registry must be UnifiedStatementRegistry or None")
    if not isinstance(proof_links, tuple) or not all(
        isinstance(link, ProofStepLink) for link in proof_links
    ):
        raise TypeError("proof_links must be a tuple of ProofStepLink")
    if proof_links and registry is None:
        raise ValueError("registry is required for proof_links")

    steps = result.proven_steps
    root_index = next(
        (i for i in range(len(steps) - 1, -1, -1)
         if result.conclusion is not None and steps[i].conclusion == result.conclusion),
        None,
    )
    references: list[LiteratureReference] = []
    associations: list[list[int]] = []
    assertion_ids: list[list[str]] = []
    per_step: list[tuple[int, ...]] = []

    for step_index, step in enumerate(steps):
        located: list[tuple[LiteratureReference, str | None]] = []
        inference_rule = step.inference_rule
        if inference_rule is not None and inference_rule.literature_reference is not None:
            located.append((inference_rule.literature_reference, None))
        if registry is not None:
            for link in proof_links:
                if link.step is None or link.step != step:
                    continue
                assertion = registry.assertion(link.assertion_id)
                entry = registry.reference(assertion.reference_id)
                located.append((LiteratureReference(label=entry.locator, locator=entry.locator), assertion.assertion_id))
        numbers: list[int] = []
        for reference, assertion_id in located:
            try:
                ref_index = references.index(reference)
            except ValueError:
                ref_index = len(references)
                references.append(reference)
                associations.append([])
                assertion_ids.append([])
            number = ref_index + 1
            if step_index not in associations[ref_index]:
                associations[ref_index].append(step_index)
            if assertion_id is not None and assertion_id not in assertion_ids[ref_index]:
                assertion_ids[ref_index].append(assertion_id)
            if number not in numbers:
                numbers.append(number)
        per_step.append(tuple(numbers))

    citations = tuple(
        NarrativeCitation(
            number=i + 1,
            reference=reference,
            step_indices=tuple(associations[i]),
            assertion_ids=tuple(assertion_ids[i]),
        )
        for i, reference in enumerate(references)
    )
    return ProofNarrativeModel(
        steps=steps,
        citations=citations,
        step_citation_numbers=tuple(per_step),
        root_index=root_index,
    )
