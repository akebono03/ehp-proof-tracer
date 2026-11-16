"""Actual typed proof-connection tests; no synthetic completed ProofSteps."""
from __future__ import annotations

from dataclasses import replace

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase175_r3r6_lemma57_general.rule import lemma57_criterion_inputs
from phase175_r3r6_lemma57_general.source import TodaLemma57GeneralCriterion
from phase175_r3r7_lemma54_membership.rule import cited_lemma54_double_relation
from phase175_r3r8r1_verified_prior_public.route import (
    prepare_pi73_public_connection,
    public_cited_ehp_extensions,
)
from proof import ProofRule


def test_pi73_prepared_provider_exposes_six_independent_goals() -> None:
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=3, k=4)
    assert len(candidates) == 1
    goal = candidates[0]
    prepared = prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id=None,
        prior_conclusions=(),
    )
    assert prepared is not None
    augmented, citing_id, provider = prepared
    assert citing_id == resolve_specialized_goal_citing_id(bridge, goal)
    assert len(provider(cited_lemma54_double_relation())) >= 1
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    zero = GeneratorImage(e, prior.rhs.generator, Zero())
    general, membership = lemma57_criterion_inputs(zero)
    for target in (
        membership, zero, ImageZeroStatement(e),
        CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order),
    ):
        assert len(provider(target)) >= 1
    assert general == TodaLemma57GeneralCriterion()
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in augmented.proof_links)
    assert ADOPTED_ID not in bridge.registry._assertions


ADOPTED_ID = "phase173:r4r1:lemma54:typed_hopf_source"


def test_wrong_or_unregistered_goal_cannot_enable_connection() -> None:
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=4)
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=replace(goal, lhs=TodaPrimaryGroup(9, 3)),
        citing_assertion_id=None, prior_conclusions=(),
    ) is None
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id="invented-id",
        prior_conclusions=(),
    ) is None


def test_public_proposals_never_directly_prove_a_goal() -> None:
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=4)
    result = prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id=None, prior_conclusions=(),
    )
    assert result is not None
    augmented, citing, provider = result
    screened = screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert available.count(TodaLemma54TypedSource()) == 1
    assert available.count(TodaLemma57GeneralCriterion()) == 1
    assert goal not in available
    extension = public_cited_ehp_extensions(available)
    for offered in extension(cited_lemma54_double_relation()):
        assert hasattr(offered, "subgoals")
        assert not hasattr(offered, "conclusion")
    assert provider(goal) is not None
