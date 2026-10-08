from homotopy_groups import (
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from toda_rules import (
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)
from phase161_backward_goal_schema import (
    BackwardGoalExpansion,
    expand_phase161_r2_suspension_isomorphism_goal,
)


def test_phase161_r2_generates_two_concrete_subgoals():
    suspension = TodaSuspensionMap(
        source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
        target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
    )
    goal = TodaSuspensionIsomorphismStatement(map=suspension)
    result = expand_phase161_r2_suspension_isomorphism_goal(goal)
    assert isinstance(result, BackwardGoalExpansion)
    assert result.goal == goal
    assert result.subgoals == (
        TodaSuspensionInjectiveStatement(map=suspension),
        TodaSuspensionSurjectiveStatement(map=suspension),
    )
    assert len(result.inference_rule.premise_patterns) == 2


def test_phase161_r2_rejects_other_suspension_map_without_fabricating_steps():
    other_map = TodaSuspensionMap(
        source_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        target_group=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4),
    )
    goal = TodaSuspensionIsomorphismStatement(map=other_map)
    assert expand_phase161_r2_suspension_isomorphism_goal(goal) is None


def test_phase161_r2_rejects_non_isomorphism_goals():
    assert expand_phase161_r2_suspension_isomorphism_goal("not a statement") is None
