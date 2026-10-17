from dataclasses import dataclass

import pytest

from homotopy_groups import TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r10_goal_driven_ehp import goal_exactness_obligations
from proof import Relation, RelationType


def test_r10_pi43_two_windows_come_from_goal_dimensions():
    goal = Relation(TodaPrimaryGroup(4, 3), "unproved structure", RelationType.EQUALITY)
    result = goal_exactness_obligations(goal)
    assert (result.prop42_n, result.prop42_i) == (2, 4)
    a, b = result.delta_e.window, result.e_h.window
    assert (a.source_term, a.middle_term, a.target_term) == (
        TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3),
    )
    assert (b.source_term, b.middle_term, b.target_term) == (
        TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3), TodaPrimaryGroup(4, 5),
    )
    assert (a.first_map, a.second_map) == (EHP_DELTA_MAP, EHP_E_MAP)
    assert (b.first_map, b.second_map) == (EHP_E_MAP, EHP_H_MAP)


def test_r10_different_goal_changes_windows_without_special_cases():
    goal = Relation(TodaPrimaryGroup(5, 4), "unproved structure", RelationType.EQUALITY)
    result = goal_exactness_obligations(goal)
    assert (result.prop42_n, result.prop42_i) == (3, 5)
    assert result.delta_e.window.source_term == TodaPrimaryGroup(6, 7)
    assert result.delta_e.window.target_term == TodaPrimaryGroup(5, 4)
    assert result.e_h.window.middle_term == TodaPrimaryGroup(5, 4)


def test_r10_no_inference_from_goal_rhs():
    first = goal_exactness_obligations(Relation(TodaPrimaryGroup(4, 3), "A", RelationType.EQUALITY))
    second = goal_exactness_obligations(Relation(TodaPrimaryGroup(4, 3), "B", RelationType.EQUALITY))
    assert first.delta_e == second.delta_e
    assert first.e_h == second.e_h


def test_r10_invalid_dimensions_fail_closed():
    with pytest.raises(ValueError):
        goal_exactness_obligations(Relation(TodaPrimaryGroup(3, 1), "x", RelationType.EQUALITY))
    with pytest.raises(ValueError):
        goal_exactness_obligations(Relation(TodaPrimaryGroup(2, 3), "x", RelationType.EQUALITY))


def test_r10_rejects_non_group_goal():
    with pytest.raises(TypeError):
        goal_exactness_obligations(Relation("not-group", "x", RelationType.EQUALITY))
