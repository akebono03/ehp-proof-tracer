"""Targeted shared typed-goal tests: no saved proof replay or group-specific dispatch."""
from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
)
from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule, Relation
from unified_statement_registry import AssertionOrigin


def _adopted_source():
    path = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    return build_adopted_typed_reference_registry(path)


def test_r9_shared_registry_contains_source_claims_not_old_completed_proof():
    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))
    assert len(bridge.proof_links) == 9
    assert all(
        entry.origin is not AssertionOrigin.PROOF_INTERNAL
        for entry in bridge.registry._assertions.values()
    )
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)


def test_r9_pi32_regenerated_by_shared_mathematical_expansion():
    from hopf_facts import ETA_2
    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))
    result = search_shared_group_goal(
        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    assert any(step.rule is ProofRule.INFERENCE for step in result.proven_steps)


def test_r9_pi43_is_a_real_typed_goal_even_if_not_proved():
    from expression import GeneratorSymbol, HomotopyElement
    eta3 = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))
    result = search_shared_group_goal(
        n=3, k=1,
        group_structure=FiniteCyclicGroup(order=2, generator=eta3),
        bridge=bridge,
    )
    assert result.status in (ProofSearchStatus.SEARCH_FAILED, ProofSearchStatus.PARTIAL)
    assert result.conclusion is None
    assert any(isinstance(goal, Relation) for goal in result.open_goals)


def test_r9_shared_expansions_no_pi32_goal_equality_branch():
    from hopf_facts import ETA_2
    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))
    expand = shared_expansion_provider(bridge)
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    options = expand(goal)
    assert options
    assert len(options[0].subgoals) == 3


def test_r9_historical_r38_proof_still_generates():
    from phase165_r14_r38_direct_registry import reconstruct_registered_pi32
    bridge, step = reconstruct_registered_pi32(
        Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    )
    assert len(bridge.proof_links) == 9
    assert step.rule is ProofRule.INFERENCE


def test_r9_public_pi32_narrative_unchanged():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(2, 1, 2, "narrative")
    body = "\n".join(
        line.prefix + " " + " ".join(seg.value for seg in line.segments)
        for line in view.rendered_lines
    )
    assert "証明対象" in body
    assert "使用する結果" in body
    assert "証明" in body
