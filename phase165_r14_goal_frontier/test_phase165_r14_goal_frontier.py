from dataclasses import replace

import pytest

from hopf_facts import ETA_2
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType
from phase165_r14_goal_frontier import (
    build_free_cyclic_group_goal,
    inspect_free_cyclic_goal,
)


def test_typed_goal_represents_pi3_2_with_eta2():
    goal = build_free_cyclic_group_goal(2, 1, ETA_2)
    assert type(goal) is Relation
    assert goal.relation_type is RelationType.EQUALITY
    assert goal.lhs == TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    assert goal.rhs == FreeCyclicGroup(generator=ETA_2)


def test_general_constructor_does_not_depend_on_first_target():
    other = build_free_cyclic_group_goal(4, 1, ETA_2)
    assert other.lhs == TodaPrimaryGroup(group_dimension=5, sphere_dimension=4)
    assert other.rhs == FreeCyclicGroup(generator=ETA_2)


@pytest.mark.parametrize("n,k", [(True, 1), (1, 1), (2, -1), (2, True)])
def test_invalid_parameters_are_rejected(n, k):
    with pytest.raises(ValueError):
        build_free_cyclic_group_goal(n, k, ETA_2)


def test_real_registry_frontier_is_fail_closed():
    result = inspect_free_cyclic_goal(2, 1, ETA_2)
    assert result.source_assertions == 117
    assert result.typed_assertions == 0
    assert result.eligible_assertions == 0
    assert result.status == "UNRESOLVED"
    assert "legacy proof selection remains disabled" in result.blocker
