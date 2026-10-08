from homotopy_groups import (
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase161_r3_backward_goal_schema import expand_phase161_r3_goal
from toda_rules import (
    TodaDeltaInjectiveStatement,
    TodaDeltaZeroStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaHopfInvariantZeroStatement,
    TodaProp42ExactnessStatement,
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def _goal():
    return TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        )
    )


def test_r3_root_and_both_ehp_branches():
    root = expand_phase161_r3_goal(_goal())
    assert root is not None
    assert tuple(type(x) for x in root.subgoals) == (
        TodaSuspensionInjectiveStatement,
        TodaSuspensionSurjectiveStatement,
    )
    branches = []
    for branch_goal in root.subgoals:
        first = expand_phase161_r3_goal(branch_goal)
        assert first is not None
        assert isinstance(first.subgoals[1], TodaProp42ExactnessStatement)
        second = expand_phase161_r3_goal(first.subgoals[0])
        assert second is not None
        assert isinstance(second.subgoals[1], TodaProp42ExactnessStatement)
        assert expand_phase161_r3_goal(second.subgoals[0]) is None
        branches.append((first, second))
    assert isinstance(branches[0][0].subgoals[0], TodaDeltaZeroStatement)
    assert isinstance(branches[0][1].subgoals[0], TodaHopfInvariantSurjectiveStatement)
    assert isinstance(branches[1][0].subgoals[0], TodaHopfInvariantZeroStatement)
    assert isinstance(branches[1][1].subgoals[0], TodaDeltaInjectiveStatement)


def test_r3_exactness_windows_are_four_distinct_required_goals():
    root = expand_phase161_r3_goal(_goal())
    windows = []
    for branch_goal in root.subgoals:
        first = expand_phase161_r3_goal(branch_goal)
        second = expand_phase161_r3_goal(first.subgoals[0])
        windows.extend((first.subgoals[1].window, second.subgoals[1].window))
    assert len(windows) == 4
    assert len(set(windows)) == 4


def test_r3_rejects_unrelated_map_without_creating_steps():
    other = TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
            target_group=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4),
        )
    )
    assert expand_phase161_r3_goal(other) is None
    assert expand_phase161_r3_goal("E is injective") is None


def test_r3_preserves_production_premise_order():
    root = expand_phase161_r3_goal(_goal())
    for branch_goal in root.subgoals:
        first = expand_phase161_r3_goal(branch_goal)
        second = expand_phase161_r3_goal(first.subgoals[0])
        for expansion in (first, second):
            patterns = expansion.inference_rule.premise_patterns
            assert len(patterns) == len(expansion.subgoals) == 2
            assert tuple(p.statement_type for p in patterns) == tuple(
                type(subgoal) for subgoal in expansion.subgoals
            )
