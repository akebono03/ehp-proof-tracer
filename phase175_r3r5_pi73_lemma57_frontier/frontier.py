"""Observe the EHP E-H proof prerequisites for pi_7^3 without new GIVENs."""
from __future__ import annotations

from expression import Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from map_property_rules import ImageZeroStatement
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase170_r3_r6_prop58_source import _source_checked_pi73_relation
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
    expand_hopf_injective_from_zero_image, hopf_injectivity_from_zero_image_inputs,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase175_r3_pi73_hopf_lift.frontier import inspect_independent_obligation
from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def inspect_ehp_injectivity_frontier() -> dict[str, object]:
    """Locate the first missing E-image proof, using actual canonical searches."""
    bridge = build_shared_typed_bridge()
    target = exact_prior_database_result(3, 4)
    if (not isinstance(target, Relation)
            or target.lhs != TodaPrimaryGroup(7, 3)
            or not isinstance(target.rhs, FiniteCyclicGroup)
            or target.rhs.order != 2
            or _source_checked_pi73_relation(bridge) != target):
        raise RuntimeError("R3R5_PI73_TYPED_TARGET_CHANGED")
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if not isinstance(citing, str) or not citing:
        raise RuntimeError("R3R5_CITING_ASSERTION_MISSING")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    if target in available:
        raise RuntimeError("R3R5_TARGET_GIVEN_FORBIDDEN")
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    lifts = expand_cited_hopf_lift(cyclic, available)
    if len(lifts) != 1:
        raise RuntimeError("R3R5_EXPECT_ONE_REVIEWED_HOPF_LIFT")
    injectivity = lifts[0].subgoals[0]
    if not isinstance(injectivity, MapInjective):
        raise RuntimeError("R3R5_EXPECT_TYPED_HOPF_INJECTIVITY")
    inputs = hopf_injectivity_from_zero_image_inputs(injectivity)
    if inputs is None or len(expand_hopf_injective_from_zero_image(injectivity)) != 1:
        raise RuntimeError("R3R5_EHP_INJECTIVITY_RULE_CHANGED")
    zero_image, exactness = inputs
    if not isinstance(zero_image, ImageZeroStatement):
        raise RuntimeError("R3R5_EXPECT_TYPED_ZERO_IMAGE")
    prior = exact_prior_database_result(2, 4)
    if (not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != TodaPrimaryGroup(6, 2)
            or not isinstance(prior.rhs, FiniteCyclicGroup)
            or prior.rhs.order != 4):
        raise RuntimeError("R3R5_PRIOR_PI62_CYCLIC_GOAL_UNAVAILABLE")
    bridge_options = expand_zero_image_from_cyclic_generator(zero_image, prior)
    if len(bridge_options) != 1:
        raise RuntimeError("R3R5_EXISTING_CYCLIC_ZERO_IMAGE_RULE_UNAVAILABLE")
    generator_goal = bridge_options[0].subgoals[1]
    if (bridge_options[0].subgoals[0] != prior
            or not isinstance(generator_goal, GeneratorImage)
            or generator_goal.map != zero_image.map
            or generator_goal.source_generator != prior.rhs.generator
            or not isinstance(generator_goal.target_generator, Zero)):
        raise RuntimeError("R3R5_ZERO_GENERATOR_IMAGE_NOT_TYPED")
    ordinary = shared_expansion_provider(screened, proof_target=target)

    def scoped(goal: object):
        if goal == zero_image:
            return bridge_options + ordinary(goal)
        return ordinary(goal)

    questions = (
        ("ehp_exactness", exactness, ordinary),
        ("lower_pi62_group", prior, ordinary),
        ("zero_generator_image", generator_goal, ordinary),
        ("zero_suspension_image", zero_image, scoped),
        ("hopf_injectivity", injectivity, scoped),
    )
    records = [
        inspect_independent_obligation(name, goal, screened, citing, provider)
        for name, goal, provider in questions
    ]
    return {
        "target": repr(target),
        "earlier_screened_givens": len(available),
        "target_direct_given_excluded": True,
        "hopf_lift_proposals": len(lifts),
        "zero_image_generic_bridge_candidates": len(bridge_options),
        "zero_image_ordinarily_offered_routes": len(ordinary(zero_image)),
        "source_lemma57_new_given": False,
        "new_mathematical_rules": 0,
        "production_modified": False,
        "obligations": records,
    }
