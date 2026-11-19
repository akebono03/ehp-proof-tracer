"""Finite cyclic zero-image inference from a linked, positioned literature GIVEN.

R40's adopted-database identity verification is intentionally untouched.
The new rule accepts only the precise linked ProofStep of a fixed literature
assertion, plus a separately inferred generator-zero image.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import group_coordinates
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    cyclic_generator_zero_image_inputs,
)
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep, Relation
from unified_statement_registry import AssertionOrigin

RULE_NAME = "linked literature cyclic presentation and generator zero imply zero image"


def verified_literature_zero_image_inputs(
    goal: object,
    presentation: object,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> tuple[tuple[Relation, GeneratorImage], ProofStep] | None:
    """Certify one exact linked earlier fixed literature assertion, not a DB row."""
    if not isinstance(bridge, RegistryBridgeResult):
        return None
    root = group_coordinates(proof_target)
    obligations = cyclic_generator_zero_image_inputs(goal, presentation)
    if root is None or obligations is None:
        return None
    domain = goal.map.source_group
    if not isinstance(domain, TodaPrimaryGroup):
        return None
    # Only strictly earlier sphere dimensions may be cited for a derived root.
    if domain.sphere_dimension >= root[0]:
        return None
    eligible = []
    for link in bridge.proof_links:
        step = link.step
        if (not isinstance(step, ProofStep)
                or step.rule is not ProofRule.GIVEN
                or step.premises
                or type(step.conclusion) is not Relation
                or step.conclusion != presentation):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        citation = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or type(assertion.content) is not Relation
                or assertion.content != presentation
                or type(reference.publication_position) is not int
                or reference.publication_position < 1
                or not isinstance(reference.locator, str)
                or not reference.locator
                or citation is None
                or citation.locator != reference.locator):
            continue
        eligible.append(step)
    if len(eligible) != 1:
        return None
    return obligations, eligible[0]


def literature_zero_image_rule(
    goal: ImageZeroStatement,
    presentation: Relation,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> InferenceRule:
    """Match the exact linked literature ProofStep and an inferred zero image."""
    verified = verified_literature_zero_image_inputs(
        goal, presentation, proof_target=proof_target, bridge=bridge,
    )
    if verified is None:
        raise ValueError("expected a uniquely linked positioned fixed literature presentation")
    obligations, witness = verified

    def guard(premises, bindings):
        current = verified_literature_zero_image_inputs(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        )
        return (
            current is not None
            and current[0] == obligations
            and current[1] == witness
            and len(premises) == 2
            and premises[0] == witness
            and premises[1].rule is ProofRule.INFERENCE
            and tuple(step.conclusion for step in premises) == obligations
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "An earlier independently positioned fixed literature assertion "
            "proves A=Z/m{g}; a separate inference proves E(g)=0. "
            "Therefore im(E)=0. The original cited GIVEN identity is retained."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                statement_pattern=obligations[0],
                proof_rule=ProofRule.GIVEN,
            ),
            PremisePattern(
                statement_type=GeneratorImage,
                statement_pattern=obligations[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_literature_zero_image(
    goal: object,
    presentation: object,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> tuple[GoalExpansion, ...]:
    verified = verified_literature_zero_image_inputs(
        goal, presentation, proof_target=proof_target, bridge=bridge,
    )
    if verified is None:
        return ()
    return (GoalExpansion(
        literature_zero_image_rule(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        ),
        verified[0],
    ),)
