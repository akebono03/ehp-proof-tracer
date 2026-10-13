import pytest

from homotopy_groups import TodaPrimaryGroup, FreeCyclicGroup
from hopf_facts import ETA_2
from phase165_r14_r34_backward_search import (
    pi32_goal, phase165_r34_expansions, trace_goal_frontier, audit_r34,
)


def test_root_goal_is_requested_pi32():
    root = pi32_goal()
    assert root.lhs == TodaPrimaryGroup(3, 2)
    assert root.rhs == FreeCyclicGroup(ETA_2)


def test_root_expands_into_three_typed_goals():
    expansions = phase165_r34_expansions(pi32_goal())
    assert len(expansions) == 1
    assert len(expansions[0].subgoals) == 3


def test_backward_frontier_reaches_unresolved_leaves():
    report = trace_goal_frontier(pi32_goal())
    assert report["derived_goal_count"] >= 1
    assert report["unresolved_leaf_count"] >= 1


def test_limit_is_fail_closed():
    with pytest.raises(ValueError):
        trace_goal_frontier(pi32_goal(), 1)


def test_no_unrelated_goal_promotion():
    assert phase165_r34_expansions(object()) == ()


def test_strict_search_remains_unproved_without_eligible_leaves():
    report = audit_r34()
    assert not report["strict_registry_proof_created"]
    assert report["source_manifest_assertions"] == 117
    assert not report["existing_proof_replay_used"]
