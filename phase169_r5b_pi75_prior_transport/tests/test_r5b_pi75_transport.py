"""R5B: prior-positioned source as proved subgoal, never an assumed GIVEN."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import PriorGroupResult, resolve_prior_group_result
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from phase169_r5b_pi75_prior_transport.rule import expand_prior_cited_toda45_composite_transport
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def pi75():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=5, k=2)
    assert len(candidates) == 1
    goal = candidates[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing is not None
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    return bridge, goal, citing, screened, available


def test_r5b_positioned_lower_source_and_unmodified_r3o_gate(pi75):
    bridge, goal, citing, screened, available = pi75
    prior = resolve_prior_group_result(
        screened, source_n=4, source_k=2, citing_assertion_id=citing,
    )
    assert prior.eligible and prior.reason == "prior_fixed_source"
    assert prior.relation is not None and prior.relation.lhs == TodaPrimaryGroup(6, 4)
    assert all(statement != prior.relation for statement in available)
    assert expand_cited_toda45_composite_transport(goal, available) == ()


def test_r5b_three_subgoals_are_obligations_not_given_steps(pi75):
    _, goal, _, screened, available = pi75
    options = expand_prior_cited_toda45_composite_transport(
        goal, available, screened, proof_target=goal,
    )
    assert len(options) == 1
    option = options[0]
    assert len(option.subgoals) == 3
    assert [type(x).__name__ for x in option.subgoals] == [
        "Relation", "Toda45IsomorphismStatement", "GeneratorImage",
    ]
    assert option.rule.name == "cited Toda (4.5) finite-cyclic composite generator transport"


def test_r5b_disallows_other_target_and_nonroot_use(pi75):
    _, goal, _, screened, available = pi75
    assert expand_prior_cited_toda45_composite_transport(
        goal, available, screened, proof_target=object(),
    ) == ()
    other = replace(goal, lhs=TodaPrimaryGroup(8, 6))
    assert expand_prior_cited_toda45_composite_transport(
        other, available, screened, proof_target=other,
    ) == ()


def test_r5b_missing_positioned_prior_source_fails_closed(pi75, monkeypatch):
    _, goal, citing, screened, available = pi75
    from phase169_r5b_pi75_prior_transport import rule as module
    def deny_prior(*args, **kwargs):
        return PriorGroupResult(4, 2, None, citing, None, False, "source_not_prior")
    monkeypatch.setattr(module, "resolve_prior_group_result", deny_prior)
    assert expand_prior_cited_toda45_composite_transport(
        goal, available, screened, proof_target=goal,
    ) == ()


def test_r5b_real_three_premise_reconstruction(pi75):
    _, goal, citing, screened, _ = pi75
    provider = shared_expansion_provider(screened, proof_target=goal)
    proof = reconstruct_registered_goal(
        goal, screened, citing, provider, lookup_mode="typed_reference_publication",
    )
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == goal
    assert len(proof.premises) == 3
    assert all(parent.rule is ProofRule.INFERENCE for parent in proof.premises)
    assert proof.premises[0].conclusion.lhs == TodaPrimaryGroup(6, 4)


def test_r5b_public_search_and_standard_web_are_complete(pi75):
    bridge, goal, _, _, _ = pi75
    contexts = []
    search = search_group_from_registered_goal(
        n=5, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert search.status is ProofSearchStatus.COMPLETE
    assert search.conclusion == goal
    assert search.open_goals == ()
    assert len(contexts) == 1
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    verify_proof_tree_for_narrative(
        search, contexts[0], citing_assertion_id=citing,
    )
    view = build_standard_web_group_proof_view(5, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == len(search.proven_steps)
