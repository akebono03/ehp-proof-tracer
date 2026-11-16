"""Earlier database premises must be verified by the actual prior-admission gate."""
from __future__ import annotations

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
)
from phase175_r3r8r1_verified_prior_public.route import prepare_pi73_public_connection
from phase175_r3r8r1_verified_prior_public.rule import (
    expand_verified_prior_hopf_lift,
    expand_verified_prior_zero_image,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation,
    find_inference_matches_for_rule,
)


def _inferred(statement: object) -> ProofStep:
    """Construct a test-only inferred premise with a nonempty ancestry."""
    return ProofStep(
        conclusion=statement,
        premises=(ProofStep(
            conclusion="test-ancestor", premises=(), rule=ProofRule.GIVEN,
        ),),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only inferred premise"),
    )


def test_verified_prior_zero_image_accepts_only_rechecked_db_step() -> None:
    bridge = build_shared_typed_bridge()
    target = exact_prior_database_result(3, 4)
    prior = exact_prior_database_result(2, 4)
    assert isinstance(target, Relation) and isinstance(prior, Relation)
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    goal = ImageZeroStatement(e)
    offers = expand_verified_prior_zero_image(
        goal, prior, proof_target=target, bridge=bridge,
    )
    assert len(offers) == 1
    option = offers[0]
    actual_db = admitted_db_step(prior, proof_target=target, bridge=bridge)
    assert actual_db is not None
    actual_image = _inferred(GeneratorImage(e, prior.rhs.generator, Zero()))
    assert len(find_inference_matches_for_rule(
        option.rule, (actual_db, actual_image),
    )) == 1
    forged_group = ProofStep(prior, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(
        option.rule, (forged_group, actual_image),
    ) == ()
    forged_image = ProofStep(actual_image.conclusion, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(
        option.rule, (actual_db, forged_image),
    ) == ()


def test_wrong_order_or_group_cannot_supply_prior() -> None:
    bridge = build_shared_typed_bridge()
    prior = exact_prior_database_result(2, 4)
    assert isinstance(prior, Relation)
    goal = ImageZeroStatement(TodaSuspensionMap(
        TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3),
    ))
    # A result cannot be its own earlier prior or be used backward in order.
    assert expand_verified_prior_zero_image(
        goal, prior, proof_target=prior, bridge=bridge,
    ) == ()
    assert expand_verified_prior_zero_image(
        goal, prior, proof_target=exact_prior_database_result(2, 1), bridge=bridge,
    ) == ()
    assert expand_verified_prior_zero_image(
        goal, object(), proof_target=exact_prior_database_result(3, 4), bridge=bridge,
    ) == ()


def test_verified_prior_hopf_lift_uses_exact_earlier_group_and_inferred_image() -> None:
    bridge = build_shared_typed_bridge()
    target, = registered_group_goal_candidates(bridge, n=3, k=4)
    prepared = prepare_pi73_public_connection(
        bridge=bridge, goal=target, citing_assertion_id=None,
        prior_conclusions=(),
    )
    assert prepared is not None
    augmented, citing, provider = prepared
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    candidates = tuple(
        option for option in provider(cyclic)
        if option.rule.name == "verified prior DB Hopf cyclic generator preimage lift"
    )
    assert len(candidates) == 1
    option = candidates[0]
    injective, group, image = option.subgoals
    assert group == exact_prior_database_result(5, 2)
    actual_db = admitted_db_step(group, proof_target=target, bridge=augmented)
    assert actual_db is not None
    parents = (_inferred(injective), actual_db, _inferred(image))
    assert len(find_inference_matches_for_rule(option.rule, parents)) == 1
    forged = ProofStep(group, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(
        option.rule, (_inferred(injective), forged, _inferred(image)),
    ) == ()
    assert find_inference_matches_for_rule(
        option.rule, (parents[0], parents[1], ProofStep(image, (), ProofRule.GIVEN)),
    ) == ()
    assert expand_verified_prior_hopf_lift(
        cyclic, group, image, proof_target=group, bridge=augmented,
    ) == ()


def test_no_new_target_given_is_injected() -> None:
    bridge = build_shared_typed_bridge()
    target, = registered_group_goal_candidates(bridge, n=3, k=4)
    prepared = prepare_pi73_public_connection(
        bridge=bridge, goal=target, citing_assertion_id=None,
        prior_conclusions=(),
    )
    assert prepared is not None
    augmented, _, provider = prepared
    assert not any(
        link.step is not None and link.step.conclusion == target
        for link in augmented.proof_links
    )
    assert all(not isinstance(option, ProofStep) for option in provider(target))
