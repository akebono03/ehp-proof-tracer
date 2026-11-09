"""Generic cyclic zero-image inference from a VERIFIED adopted earlier DB prior.

This does not convert the DB prior to a literature reference or an INFERENCE.
The R6 inference-only rule is unchanged.  Every application revalidates the
actual adopted database step against the independently specified proof root.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    group_coordinates,
    verified_db_step,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    cyclic_generator_zero_image_inputs,
)
from proof import InferenceRule, PremisePattern, ProofRule, Relation
from phase165_r14_r6_generic_iso import GeneratorImage
from map_property_rules import ImageZeroStatement


RULE_NAME = "adopted earlier DB cyclic presentation and inferred generator zero imply zero image"


def verified_prior_zero_image_inputs(
    goal: object,
    presentation: object,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> tuple[Relation, GeneratorImage] | None:
    """Accept a real earlier adopted DB row as an obligation, never as a theorem.

    The generator, cyclic order, E dimensions and root's precedence are all
    rechecked by the existing independent admission mechanism.  No conversion
    of a GIVEN into an INFERENCE is performed here.
    """
    if (not isinstance(bridge, RegistryBridgeResult)
            or group_coordinates(proof_target) is None):
        return None
    obligations = cyclic_generator_zero_image_inputs(goal, presentation)
    if obligations is None:
        return None
    admitted = admitted_db_step(presentation, proof_target=proof_target, bridge=bridge)
    if (admitted is None
            or admitted.rule is not ProofRule.GIVEN
            or not verified_db_step(admitted, proof_target=proof_target, bridge=bridge)):
        return None
    return obligations


def adopted_prior_zero_image_rule(
    goal: ImageZeroStatement,
    presentation: Relation,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> InferenceRule:
    """Derive zero image only from a verified DB GIVEN and an inferred zero image of g."""
    obligations = verified_prior_zero_image_inputs(
        goal, presentation, proof_target=proof_target, bridge=bridge,
    )
    if obligations is None:
        raise ValueError("Not an eligible earlier adopted cyclic DB presentation")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[1].rule is ProofRule.INFERENCE
            and tuple(step.conclusion for step in premises) == obligations
            and verified_db_step(premises[0], proof_target=proof_target, bridge=bridge)
            and verified_prior_zero_image_inputs(
                goal, presentation, proof_target=proof_target, bridge=bridge,
            ) == obligations
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "A verified, explicitly adopted earlier DB presentation Z/m{g}, "
            "and a separate proved E(g)=0, imply im(E)=0. The DB premise "
            "remains an adopted GIVEN, not a cited Toda fact or an inference. "
            "Every application checks the original DB and strict root precedence."
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
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_adopted_prior_zero_image(
    goal: object,
    presentation: object,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> tuple[GoalExpansion, ...]:
    """Return an isolated backward candidate, not a proof or a GIVEN."""
    obligations = verified_prior_zero_image_inputs(
        goal, presentation, proof_target=proof_target, bridge=bridge,
    )
    if obligations is None:
        return ()
    return (GoalExpansion(
        adopted_prior_zero_image_rule(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        ),
        obligations,
    ),)
