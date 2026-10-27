"""R6A: genuine four-obligation E^2 transport; never cite pi_7^5 as GIVEN."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import PriorGroupResult, resolve_prior_group_result
from phase169_r6a_pi86_two_step_transport.rule import (
    _two_step_eta_square_images,
    expand_prior_two_step_eta_square_transport,
)
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule
from toda_rules import Toda45IsomorphismStatement
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def boundary():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=6, k=2)
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


def test_r6a_source_is_prior_and_intermediate_result_is_not_prior(boundary):
    _, goal, citing, screened, available = boundary
    lower = resolve_prior_group_result(
        screened, source_n=4, source_k=2, citing_assertion_id=citing,
    )
    middle = resolve_prior_group_result(
        screened, source_n=5, source_k=2, citing_assertion_id=citing,
    )
    assert lower.eligible and lower.reason == "prior_fixed_source"
    assert middle.reason == "source_not_prior" and not middle.eligible
    assert lower.relation is not None and lower.relation not in available
    options = expand_prior_two_step_eta_square_transport(
        goal, available, screened, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == lower.relation
    assert len(options[0].subgoals) == 4
    assert all(
        not (hasattr(premise, "lhs") and premise.lhs == TodaPrimaryGroup(7, 5))
        for premise in options[0].subgoals
    )


def test_r6a_two_generator_images_are_exact_adjacent_proof_goals(boundary):
    _, goal, _, screened, available = boundary
    subgoals = expand_prior_two_step_eta_square_transport(
        goal, available, screened, proof_target=goal,
    )[0].subgoals
    lower, iso, first, second = subgoals
    assert iso.map.exponent == 2
    assert iso.map.source_group == lower.lhs
    assert iso.map.target_group == goal.lhs
    assert isinstance(first, GeneratorImage) and isinstance(second, GeneratorImage)
    assert first.target_generator == second.source_generator
    assert first.map.source_group == lower.lhs
    assert first.map.target_group == TodaPrimaryGroup(7, 5)
    assert second.map.source_group == TodaPrimaryGroup(7, 5)
    assert second.map.target_group == goal.lhs
    assert _two_step_eta_square_images(lower, goal) == (first, second)


def test_r6a_proof_rule_needs_all_four_matching_premises(boundary):
    _, goal, _, screened, available = boundary
    candidate = expand_prior_two_step_eta_square_transport(
        goal, available, screened, proof_target=goal,
    )[0]
    premises = tuple(ProofStep(
        conclusion=assertion, premises=(), rule=ProofRule.INFERENCE,
    ) for assertion in candidate.subgoals)
    match = find_inference_matches_for_rule(candidate.rule, premises)
    assert len(match) == 1
    derived = apply_inference_match(match[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == premises
    bad_given = premises[:3] + (replace(premises[3], rule=ProofRule.GIVEN),)
    assert find_inference_matches_for_rule(candidate.rule, bad_given) == ()
    bad_image = premises[:3] + (replace(
        premises[3], conclusion=replace(
            premises[3].conclusion,
            target_generator=premises[2].conclusion.source_generator,
        ),
    ),)
    assert find_inference_matches_for_rule(candidate.rule, bad_image) == ()


def test_r6a_missing_cited_toda45_or_different_target_fails_closed(boundary):
    _, goal, _, screened, available = boundary
    without_iso = tuple(
        claim for claim in available if not isinstance(claim, Toda45IsomorphismStatement)
    )
    assert expand_prior_two_step_eta_square_transport(
        goal, without_iso, screened, proof_target=goal,
    ) == ()
    assert expand_prior_two_step_eta_square_transport(
        goal, available, screened, proof_target=object(),
    ) == ()
    other = replace(goal, lhs=TodaPrimaryGroup(9, 7))
    assert expand_prior_two_step_eta_square_transport(
        other, available, screened, proof_target=other,
    ) == ()


def test_r6a_missing_prior_source_fails_closed(boundary, monkeypatch):
    _, goal, citing, screened, available = boundary
    from phase169_r6a_pi86_two_step_transport import rule as module

    def unavailable(*args, **kwargs):
        return PriorGroupResult(4, 2, None, citing, None, False, "source_not_prior")

    monkeypatch.setattr(module, "resolve_prior_group_result", unavailable)
    assert expand_prior_two_step_eta_square_transport(
        goal, available, screened, proof_target=goal,
    ) == ()


def test_r6a_canonical_search_and_web_complete_without_pi75_group_given(boundary):
    bridge, goal, citing, _, _ = boundary
    contexts = []
    result = search_group_from_registered_goal(
        n=6, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == goal
    assert result.open_goals == ()
    assert len(contexts) == 1
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    root = result.proven_steps[-1]
    assert root.conclusion == goal
    assert root.rule is ProofRule.INFERENCE
    assert len(root.premises) == 4
    assert all(parent.rule is ProofRule.INFERENCE for parent in root.premises[1:])
    assert not any(
        step.rule is ProofRule.GIVEN
        and getattr(step.conclusion, "lhs", None) == TodaPrimaryGroup(7, 5)
        for step in result.proven_steps
    )
    web = build_standard_web_group_proof_view(6, 2, mode="narrative")
    assert web.key == "generic-complete-proof"
    assert not web.partial_result
    assert len(web.steps) == len(result.proven_steps)
