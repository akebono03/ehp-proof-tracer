"""Focused R53 regression checks; no complete-proof assumption."""
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase165_r53_pi32_goal_audit import audit_pi32_explicit_goal, pi32_explicit_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge


def test_r53_explicit_goal_preserves_generator():
    goal = pi32_explicit_goal()
    assert goal.lhs == TodaPrimaryGroup(3, 2)
    assert goal.rhs == FreeCyclicGroup(ETA_2)


def test_r53_observes_shared_search_without_mutating_links():
    bridge = build_shared_typed_bridge()
    before = tuple(bridge.proof_links)
    result = audit_pi32_explicit_goal(bridge)
    assert tuple(bridge.proof_links) == before
    assert result.status in ("complete", "partial", "search_failed")
    assert result.complete == (result.status == "complete")
    assert result.full_pytest_run is False
