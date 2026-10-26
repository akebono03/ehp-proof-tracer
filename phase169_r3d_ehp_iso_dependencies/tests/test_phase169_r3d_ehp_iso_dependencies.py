"""Focused checks for existing EHP dependency contracts (no proof fabrication)."""
from homotopy_groups import (
    TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from phase161_r4_literature_premise_matching import expand_phase161_r4_literature_goal
from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement


def _iso():
    return TodaSuspensionIsomorphismStatement(TodaSuspensionMap(
        TodaPrimaryGroup(4, 2), TodaPrimaryGroup(5, 3),
    ))


def test_historical_ehp_root_requires_both_map_properties():
    options = expand_registered_ehp_goal(_iso())
    assert len(options) == 1
    assert [type(x).__name__ for x in options[0].subgoals] == [
        "TodaSuspensionInjectiveStatement", "TodaSuspensionSurjectiveStatement",
    ]


def test_historical_ehp_branches_require_four_distinct_exactness_windows():
    root, = expand_registered_ehp_goal(_iso())
    windows = []
    for map_property in root.subgoals:
        first, = expand_registered_ehp_goal(map_property)
        second, = expand_registered_ehp_goal(first.subgoals[0])
        for expansion in (first, second):
            exactness = expansion.subgoals[1]
            assert isinstance(exactness, TodaProp42ExactnessStatement)
            windows.append(exactness.window)
    assert len(set(windows)) == 4


def test_historical_literature_terminals_require_inferred_not_given_steps():
    root, = expand_registered_ehp_goal(_iso())
    for map_property in root.subgoals:
        first, = expand_registered_ehp_goal(map_property)
        second, = expand_registered_ehp_goal(first.subgoals[0])
        literature = expand_phase161_r4_literature_goal(second.subgoals[0])
        assert literature is not None
        assert literature.requirements
        assert all(req.proof_rule is ProofRule.INFERENCE
                   for req in literature.requirements)


def test_unrelated_suspension_map_is_not_a_historical_certificate():
    other = TodaSuspensionIsomorphismStatement(TodaSuspensionMap(
        TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4),
    ))
    assert expand_registered_ehp_goal(other) == ()
