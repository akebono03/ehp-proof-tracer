"""Generic provenance-checked prior-DB variants of existing EHP group rules.

These are not new mathematical conclusions: they permit an independently
admitted, strictly earlier DB group presentation in a proof premise where
the original inference-only rule cannot apply. A zero generator image, a
Hopf injectivity, and a Hopf generator image must still be independently
proved by the canonical recursive proof search.
"""
from __future__ import annotations

from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    cyclic_generator_zero_image_inputs,
)
from phase175_r3_pi73_hopf_lift.rule import hopf_lift_inputs
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from map_property_rules import ImageZeroStatement


def verified_prior_zero_image_rule(
    goal: ImageZeroStatement,
    presentation: Relation,
    *,
    proof_target: object,
    bridge: object,
) -> InferenceRule:
    """Use a strictly earlier, freshly verified DB group with inferred E(g)=0."""
    required = cyclic_generator_zero_image_inputs(goal, presentation)
    if required is None:
        raise ValueError("invalid cyclic zero-image obligation")
    if admitted_db_step(presentation, proof_target=proof_target, bridge=bridge) is None:
        raise ValueError("cyclic source is not an earlier admitted DB group")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[1].rule is ProofRule.INFERENCE
            and bool(premises[1].premises)
            and tuple(p.conclusion for p in premises) == required
            and verified_db_step(
                premises[0], proof_target=proof_target, bridge=bridge,
            )
            and cyclic_generator_zero_image_inputs(goal, presentation) == required
        )

    return InferenceRule(
        name="verified prior DB finite-cyclic generator zero implies zero image",
        description=(
            "For a group already admitted under strict prior-DB ordering, "
            "the separately inferred zero image of its cyclic generator "
            "forces the suspension homomorphism to have zero image. "
            "The actual adopted group premise is reverified on application."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=presentation,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=required[1],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_verified_prior_zero_image(
    goal: object,
    presentation: object,
    *,
    proof_target: object,
    bridge: object,
) -> tuple[GoalExpansion, ...]:
    """Build a candidate only when the real earlier group is admissible."""
    required = cyclic_generator_zero_image_inputs(goal, presentation)
    if required is None:
        return ()
    if admitted_db_step(presentation, proof_target=proof_target, bridge=bridge) is None:
        return ()
    return (GoalExpansion(
        verified_prior_zero_image_rule(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        ),
        required,
    ),)


def verified_prior_hopf_lift_rule(
    goal: CyclicStructureStatement,
    codomain: Relation,
    image: Relation,
    *,
    proof_target: object,
    bridge: object,
) -> InferenceRule:
    """Hopf cyclic generator lift with a proven H and earlier adopted codomain."""
    required = hopf_lift_inputs(goal, codomain, image)
    if required is None:
        raise ValueError("invalid Hopf lift obligations")
    if admitted_db_step(codomain, proof_target=proof_target, bridge=bridge) is None:
        raise ValueError("Hopf codomain is not an earlier admitted DB group")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.INFERENCE
            and bool(premises[0].premises)
            and premises[1].rule is ProofRule.GIVEN
            and premises[2].rule is ProofRule.INFERENCE
            and bool(premises[2].premises)
            and tuple(p.conclusion for p in premises) == required
            and verified_db_step(
                premises[1], proof_target=proof_target, bridge=bridge,
            )
            and hopf_lift_inputs(goal, codomain, image) == required
        )

    return InferenceRule(
        name="verified prior DB Hopf cyclic generator preimage lift",
        description=(
            "An independently proved injective Hopf map whose separately "
            "inferred generator image generates its strictly earlier, "
            "reverified finite-cyclic DB codomain gives the cyclic domain "
            "with the same generator and order."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=MapInjective,
                statement_pattern=required[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=codomain,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_verified_prior_hopf_lift(
    goal: object,
    codomain: object,
    image: object,
    *,
    proof_target: object,
    bridge: object,
) -> tuple[GoalExpansion, ...]:
    """Use registered Hopf image and an admissible older DB group as goals."""
    required = hopf_lift_inputs(goal, codomain, image)
    if required is None:
        return ()
    if admitted_db_step(codomain, proof_target=proof_target, bridge=bridge) is None:
        return ()
    return (GoalExpansion(
        verified_prior_hopf_lift_rule(
            goal, codomain, image,
            proof_target=proof_target, bridge=bridge,
        ),
        required,
    ),)
