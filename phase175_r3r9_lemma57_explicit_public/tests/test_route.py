"""The public provider must use the specific cited clause, not Lemma 5.4."""
from __future__ import annotations

from dataclasses import replace

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r3r9_lemma57_explicit_public.route import (
    prepare_pi73_public_connection,
)
from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME
from phase175_r3r9_lemma57_explicit_public.source import (
    ASSERTION_ID,
    TodaLemma57ExplicitNuPrimeZero,
)
from proof import ProofRule


def test_prepared_route_uses_explicit_lemma_without_lemma54() -> None:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=4)
    assert len(goals) == 1
    goal = goals[0]
    prepared = prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id=None,
        prior_conclusions=(),
    )
    assert prepared is not None
    augmented, citing, provider = prepared
    assert citing == resolve_specialized_goal_citing_id(bridge, goal)
    assert ASSERTION_ID in augmented.registry._assertions
    assert ASSERTION_ID not in bridge.registry._assertions
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in augmented.proof_links)
    links = [link for link in augmented.proof_links
             if link.step is not None
             and link.step.conclusion == TodaLemma57ExplicitNuPrimeZero()]
    assert len(links) == 1
    assert links[0].step.rule is ProofRule.GIVEN
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    image = GeneratorImage(e, prior.rhs.generator, Zero())
    options = provider(image)
    assert options[0].rule.name == RULE_NAME
    assert not any("Lemma 5.4" in option.rule.name for option in options)


def test_wrong_registered_target_cannot_trigger_route() -> None:
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=4)
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=replace(goal, lhs=TodaPrimaryGroup(9, 3)),
        citing_assertion_id=None, prior_conclusions=(),
    ) is None
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id="fabricated-citation",
        prior_conclusions=(),
    ) is None
