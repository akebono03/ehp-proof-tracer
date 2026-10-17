"""Generic proof-backed first-isomorphism -> cyclic quotient -> group relation.

Only actual ProofStep premises are accepted. This module supplies no literature
facts, no target-specific adapters, and no synthetic GIVEN steps.
"""
from __future__ import annotations

from dataclasses import dataclass

from map_property_rules import SurjectiveMapStatement
from phase165_r12_r2_quotient_rules import (
    CyclicStructureStatement,
    HomomorphismPresentationStatement,
    KernelMultipleStatement,
    first_isomorphism_quotient_inference_rule,
    infinite_cyclic_quotient_structure_inference_rule,
)
from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


@dataclass(frozen=True)
class QuotientChainResult:
    status: str
    proof: ProofStep | None
    blocker: str | None
    intermediate_steps: tuple[ProofStep, ...]


def _derive(rule, premises: tuple[ProofStep, ...]) -> ProofStep | None:
    if any(not isinstance(step, ProofStep) for step in premises):
        raise TypeError("all premises must be actual ProofStep objects")
    matches = tuple(
        item for item in find_inference_matches_for_rule(rule, premises)
        if len(item.premises) == len(premises)
        and all(left is right for left, right in zip(item.premises, premises))
    )
    if len(matches) != 1:
        return None
    step = apply_inference_match(matches[0])
    if step.rule is not ProofRule.INFERENCE or step.premises != premises:
        return None
    return step


def build_generic_quotient_chain(
    presentation: ProofStep,
    kernel: ProofStep,
    surjectivity: ProofStep,
    source_structure: ProofStep,
) -> QuotientChainResult:
    """Derive a finite cyclic group relation from four *proved* premises.

    GIVEN inputs are supported for general unit tests, but certification must
    separately verify the provenance and eligibility of every input proof.
    """
    premises = (presentation, kernel, surjectivity, source_structure)
    if any(not isinstance(step, ProofStep) for step in premises):
        raise TypeError("four actual ProofStep premises required")
    if not isinstance(presentation.conclusion, HomomorphismPresentationStatement):
        return QuotientChainResult("UNRESOLVED", None, "presentation statement missing", ())
    if not isinstance(kernel.conclusion, KernelMultipleStatement):
        return QuotientChainResult("UNRESOLVED", None, "kernel statement missing", ())
    if not isinstance(surjectivity.conclusion, SurjectiveMapStatement):
        return QuotientChainResult("UNRESOLVED", None, "surjectivity statement missing", ())
    if not isinstance(source_structure.conclusion, CyclicStructureStatement):
        return QuotientChainResult("UNRESOLVED", None, "cyclic source structure missing", ())
    quotient = _derive(first_isomorphism_quotient_inference_rule(), premises[:3])
    if quotient is None:
        return QuotientChainResult("UNRESOLVED", None, "first isomorphism premises do not match", ())
    cyclic = _derive(infinite_cyclic_quotient_structure_inference_rule(), (quotient, source_structure))
    if cyclic is None:
        return QuotientChainResult("UNRESOLVED", None, "infinite cyclic quotient premises do not match", (quotient,))
    group = _derive(finite_cyclic_structure_as_relation_inference_rule(), (cyclic,))
    if group is None:
        return QuotientChainResult("UNRESOLVED", None, "group relation rule cannot match", (quotient, cyclic))
    return QuotientChainResult("DERIVED_NOT_PROVENANCE_CERTIFIED", group, None, (quotient, cyclic, group))
