"""Focused real-repository tests for the generalized typed Toda (5.2) route."""
from types import SimpleNamespace

import pytest

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r2_toda52_transport import (
    _eta2_right_generator,
    expand_toda52_finite_cyclic_goal,
)
from proof import Relation, RelationType


def _pi5_source_and_goal():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=2, k=3)
    assert len(candidates) == 1
    goal = candidates[0]
    assertion_id = resolve_specialized_goal_citing_id(bridge, goal)
    assert assertion_id is not None
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=assertion_id,
        explicit_publication_target=True,
    )
    available = tuple(link.step.conclusion for link in screened.proof_links if link.step is not None)
    return goal, available


def test_r3r5_pi5_goal_is_typed_eta2_composition():
    goal, _available = _pi5_source_and_goal()
    assert goal.lhs == TodaPrimaryGroup(5, 2)
    assert isinstance(goal.rhs, FiniteCyclicGroup)
    assert goal.rhs.order == 2
    assert _eta2_right_generator(goal) is not None


def test_r3r5_pi5_only_uses_screened_source_and_theorem():
    goal, available = _pi5_source_and_goal()
    options = expand_toda52_finite_cyclic_goal(goal, available)
    assert options
    assert all(len(item.subgoals) == 2 for item in options)
    assert all(item.subgoals[0].lhs == TodaPrimaryGroup(5, 3) for item in options)
    assert all(item.subgoals[1] in available for item in options)
    assert all(item.subgoals[0] in available for item in options)


def test_r3r5_cannot_assume_a_missing_source():
    goal, _ = _pi5_source_and_goal()
    assert expand_toda52_finite_cyclic_goal(goal, (Toda52UniversalStatement(),)) == ()


def test_r3r5_cannot_assume_an_uncited_theorem():
    goal, available = _pi5_source_and_goal()
    only_sources = tuple(value for value in available if not isinstance(value, Toda52UniversalStatement))
    assert expand_toda52_finite_cyclic_goal(goal, only_sources) == ()


def test_r3r5_inference_guard_checks_both_actual_premises():
    goal, available = _pi5_source_and_goal()
    expansion = expand_toda52_finite_cyclic_goal(goal, available)[0]
    source, theorem = expansion.subgoals
    guard = expansion.rule.match_guard
    assert guard((SimpleNamespace(conclusion=source), SimpleNamespace(conclusion=theorem)), {})
    wrong_source = Relation(TodaPrimaryGroup(6, 3), source.rhs, RelationType.EQUALITY)
    assert not guard((SimpleNamespace(conclusion=wrong_source), SimpleNamespace(conclusion=theorem)), {})


@pytest.mark.parametrize("m,k", [(5,3),(6,4),(7,5),(8,6)])
def test_r3r5_same_typed_entry_for_every_cyclic_n2_goal(m, k):
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=k)
    assert len(goals) == 1
    assert goals[0].lhs == TodaPrimaryGroup(m, 2)
    assert _eta2_right_generator(goals[0]) is not None
