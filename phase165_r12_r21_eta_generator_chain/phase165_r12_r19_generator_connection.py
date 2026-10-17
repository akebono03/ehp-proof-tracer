"""R12-R19: typed, premise-preserving generator suspension presentation.

A GeneratorSuspension is a premise, not a new adopted reference. This module
never creates a GIVEN step or guesses a generator witness.
"""
from __future__ import annotations

from homotopy_groups import TodaSuspensionMap
from phase165_r12_r2_quotient_rules import HomomorphismPresentationStatement
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofStep, ProofRule, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def generator_suspension_presentation_rule() -> InferenceRule:
    """Turn a proved generator suspension into a homomorphism presentation."""
    def guard(premises, bindings):
        if len(premises) != 1:
            return False
        witness = premises[0].conclusion
        return (
            isinstance(witness, GeneratorSuspension)
            and isinstance(witness.map, TodaSuspensionMap)
            and witness.map.source_group is not None
            and witness.map.target_group is not None
        )

    def build(premises):
        witness = premises[0].conclusion
        return HomomorphismPresentationStatement(
            witness.map, witness.map.source_group, witness.map.target_group,
            witness.source_generator, witness.target_generator,
        )

    return InferenceRule(
        name="generator suspension implies suspension homomorphism presentation",
        description="Suspension is a homomorphism; a proven image of one generator specifies its presentation.",
        premise_patterns=(PremisePattern(statement_type=GeneratorSuspension),),
        match_guard=guard,
        conclusion_builder=build,
    )


def expand_generator_presentation(goal: object) -> tuple[GoalExpansion, ...]:
    """Construct only a proof obligation, never its source witness."""
    if not isinstance(goal, HomomorphismPresentationStatement):
        return ()
    mapping = goal.map
    if (not isinstance(mapping, TodaSuspensionMap)
            or mapping.source_group != goal.domain
            or mapping.target_group != goal.codomain):
        return ()
    witness = GeneratorSuspension(mapping, goal.source_generator, goal.target_generator)
    return (GoalExpansion(generator_suspension_presentation_rule(), (witness,)),)


def derive_presentation_from_witness(step: ProofStep) -> ProofStep:
    """Keep a real witness as the only premise in the derived ProofStep."""
    if not isinstance(step, ProofStep) or not isinstance(step.conclusion, GeneratorSuspension):
        raise TypeError("a proved GeneratorSuspension ProofStep is required")
    if step.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE):
        raise ValueError("generator witness is not a proved source or inference")
    rule = generator_suspension_presentation_rule()
    matches = find_inference_matches_for_rule(rule, (step,))
    if len(matches) != 1:
        raise ValueError("generator suspension witness does not match")
    return derive_inference_proof_step(matches[0])
