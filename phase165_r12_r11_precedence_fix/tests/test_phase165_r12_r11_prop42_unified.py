"""Phase 165 R12-R11: unified EHP source and actual inferred specializations."""
from __future__ import annotations

from dataclasses import replace

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import (
    GENERAL_ASSERTION_ID, TodaProp42GeneralExactnessStatement,
    build_adopted_prop42_general_reference, build_prop42_specialization_provider,
    expand_cited_prop42_exactness, prop42_exactness_indices,
    prefer_universal_prop42_derivation,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r18_proof_order import ProofUseOrder, restrict_by_proof_use_order
from phase165_r3_recursive_search import reconstruct_registered_goal
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaProp42ExactnessStatement


def window(a, b, c, first, second):
    return TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        TodaPrimaryGroup(*a), TodaPrimaryGroup(*b), TodaPrimaryGroup(*c), first, second,
    ))


def test_r11_single_source_registered_once_with_reference():
    bridge = build_shared_typed_bridge()
    sources = [link for link in bridge.proof_links
               if link.step and isinstance(link.step.conclusion, TodaProp42GeneralExactnessStatement)]
    assert len(sources) == 1
    assert sources[0].step.rule is ProofRule.GIVEN
    assert bridge.registry.reference(bridge.registry.assertion(sources[0].assertion_id).reference_id).locator == "Proposition 4.2 (4.4)"


def test_r11_pi32_pi43_and_h_delta_use_one_rule():
    goals = (
        window((3,3), (1,1), (2,2), EHP_DELTA_MAP, EHP_E_MAP),
        window((2,1), (3,2), (3,3), EHP_E_MAP, EHP_H_MAP),
        window((3,2), (3,3), (1,1), EHP_H_MAP, EHP_DELTA_MAP),
        window((5,5), (3,2), (4,3), EHP_DELTA_MAP, EHP_E_MAP),
        window((3,2), (4,3), (4,5), EHP_E_MAP, EHP_H_MAP),
    )
    bridge = build_adopted_prop42_general_reference()
    source_step, = (link.step for link in bridge.proof_links)
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from proof import find_inference_matches_for_rule
    provider = build_prop42_specialization_provider(bridge)
    for goal in goals:
        options = provider(goal)
        assert len(options) == 1
        expansion = options[0]
        assert expansion.subgoals == (source_step.conclusion,)
        matches = find_inference_matches_for_rule(expansion.rule, (source_step,))
        assert len(matches) == 1
        derived = derive_inference_proof_step(matches[0])
        assert derived.rule is ProofRule.INFERENCE
        assert derived.conclusion == goal
        assert len(derived.premises) == 1
        assert derived.premises[0].rule is ProofRule.GIVEN


def test_r11_malformed_and_uncited_windows_rejected():
    wrong = window((5,5), (3,2), (4,4), EHP_DELTA_MAP, EHP_E_MAP)
    assert prop42_exactness_indices(wrong) is None
    assert expand_cited_prop42_exactness(wrong, (TodaProp42GeneralExactnessStatement(),)) == ()
    valid = window((5,5), (3,2), (4,3), EHP_DELTA_MAP, EHP_E_MAP)
    assert expand_cited_prop42_exactness(valid, ()) == ()


def test_r11_common_screened_backward_search_for_both_groups():
    bridge = build_shared_typed_bridge()
    goal = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    context_id = next(x.assertion_id for x in bridge.registry._assertions.values()
                      if x.assertion_id != "shared:5:" + GENERAL_ASSERTION_ID)
    screened = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=context_id)
    source_steps = [link.step for link in screened.proof_links
                    if isinstance(link.step.conclusion, TodaProp42GeneralExactnessStatement)]
    assert len(source_steps) == 1
    screened = prefer_universal_prop42_derivation(screened)
    provider = build_prop42_specialization_provider(screened)
    for exactness in (
        window((2,1), (3,2), (3,3), EHP_E_MAP, EHP_H_MAP),
        window((5,5), (3,2), (4,3), EHP_DELTA_MAP, EHP_E_MAP),
    ):
        step = reconstruct_registered_goal(
            exactness, screened, citing_assertion_id=context_id,
            expansion_provider=provider, lookup_mode="typed_reference",
        )
        assert step.rule is ProofRule.INFERENCE
        assert step.conclusion == exactness


def test_r11_explicit_proof_use_order_can_exclude_the_source():
    bridge = build_shared_typed_bridge()
    target_id = next(x.assertion_id for x in bridge.registry._assertions.values()
                     if ":toda:adopted:prop5.1:finite_dimensional" in x.assertion_id)
    goal = bridge.registry.assertion(target_id).content
    screened = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=target_id)
    policy = ProofUseOrder(target_assertion_id=target_id)
    restricted = restrict_by_proof_use_order(screened, goal=goal, policy=policy)
    assert not any(isinstance(x.step.conclusion, TodaProp42GeneralExactnessStatement)
                   for x in restricted.proof_links if x.step)
    exactness = window((5,5), (3,2), (4,3), EHP_DELTA_MAP, EHP_E_MAP)
    assert build_prop42_specialization_provider(restricted)(exactness) == ()


def test_r11_precedence_preserves_old_leaves_without_screened_general_source():
    bridge = build_shared_typed_bridge()
    target_id = next(x.assertion_id for x in bridge.registry._assertions.values()
                     if ":toda:adopted:prop5.1:finite_dimensional" in x.assertion_id)
    goal = bridge.registry.assertion(target_id).content
    screened = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=target_id)
    restricted = restrict_by_proof_use_order(
        screened, goal=goal, policy=ProofUseOrder(target_assertion_id=target_id)
    )
    assert prefer_universal_prop42_derivation(restricted) is restricted


def test_r11_precedence_removes_only_specialized_windows_after_screening():
    bridge = build_shared_typed_bridge()
    goal = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    context_id = next(x.assertion_id for x in bridge.registry._assertions.values()
                      if x.assertion_id != "shared:5:" + GENERAL_ASSERTION_ID)
    screened = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=context_id)
    before = [link for link in screened.proof_links
              if link.step and isinstance(link.step.conclusion, TodaProp42ExactnessStatement)]
    assert before
    chosen = prefer_universal_prop42_derivation(screened)
    after = [link for link in chosen.proof_links
             if link.step and isinstance(link.step.conclusion, TodaProp42ExactnessStatement)]
    assert not after
    assert all(link in chosen.proof_links for link in screened.proof_links
               if link.step and not isinstance(link.step.conclusion, TodaProp42ExactnessStatement))
