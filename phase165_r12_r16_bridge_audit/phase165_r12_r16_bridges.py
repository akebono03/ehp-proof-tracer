"""Generic, provenance-preserving conversion of EHP proofs to quotient premises.

No target group structure, generator image, or homomorphism is assumed.
"""
from __future__ import annotations

from expression import Multiple
from map_property_rules import SurjectiveMapStatement
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r14_r6_generic_iso import MapSurjective
from proof import InferenceRule, PremisePattern, ProofStep, apply_inference_match, find_inference_matches_for_rule


def suspension_surjectivity_as_generic_surjectivity_rule() -> InferenceRule:
    def build(premises):
        return SurjectiveMapStatement(premises[0].conclusion.map)

    return InferenceRule(
        name="certified map surjectivity entails generic surjectivity",
        premise_patterns=(PremisePattern(statement_type=MapSurjective),),
        conclusion_builder=build,
    )


def concrete_cyclic_kernel_as_multiple_rule() -> InferenceRule:
    def guard(premises, bindings):
        item = premises[0].conclusion
        generator = getattr(item.kernel_group, "generator", None)
        multiple = getattr(generator, "coefficient", None)
        source = getattr(generator, "expression", None)
        return (
            isinstance(generator, Multiple)
            and type(multiple) is int and multiple > 0
            and source is not None
            and getattr(item.map, "source_group", None) is not None
        )

    def build(premises):
        item = premises[0].conclusion
        generator = item.kernel_group.generator
        return KernelMultipleStatement(
            item.map, item.map.source_group, generator.expression, generator.coefficient,
        )

    return InferenceRule(
        name="certified cyclic suspension kernel entails kernel multiple",
        premise_patterns=(PremisePattern(statement_type=SuspensionKernelFreeCyclicStatement),),
        match_guard=guard,
        conclusion_builder=build,
    )


def derive_from_certified_proof(rule: InferenceRule, proof: ProofStep) -> ProofStep:
    """Reconstruct one inference from an existing proof, never from a bare goal."""
    if not isinstance(proof, ProofStep):
        raise TypeError("A certified ProofStep is required")
    matches = find_inference_matches_for_rule(rule, (proof,))
    if len(matches) != 1:
        raise ValueError("Expected exactly one supported inference match")
    return apply_inference_match(matches[0])
