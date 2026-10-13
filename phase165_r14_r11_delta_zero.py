"""R14-R11: generic exactness + suspension isomorphism => Delta=0."""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement


def _matching_delta_exactness(premises, bindings):
    isomorphism, exactness = (step.conclusion for step in premises)
    if (not isinstance(isomorphism, TodaSuspensionIsomorphismStatement)
            or not isinstance(exactness, TodaProp42ExactnessStatement)):
        return False
    suspension = isomorphism.map
    window = exactness.window
    return (
        isinstance(suspension, TodaSuspensionMap)
        and window.first_map == EHP_DELTA_MAP
        and window.second_map == EHP_E_MAP
        and suspension.source_group == window.middle_term
        and suspension.target_group == window.target_term
        and window.target_term.group_dimension == window.middle_term.group_dimension + 1
        and window.target_term.sphere_dimension == window.middle_term.sphere_dimension + 1
    )


def _delta_zero_conclusion(premises):
    window = premises[1].conclusion.window
    return TodaDeltaZeroStatement(
        map=TodaDeltaMap(
            source_group=window.source_term,
            target_group=window.middle_term,
        )
    )


def delta_zero_from_suspension_iso_and_exactness_rule():
    return InferenceRule(
        name="EHP: suspension isomorphism plus Delta-E exactness implies Delta zero",
        premise_patterns=(
            PremisePattern(statement_type=TodaSuspensionIsomorphismStatement),
            PremisePattern(statement_type=TodaProp42ExactnessStatement),
        ),
        match_guard=_matching_delta_exactness,
        conclusion_builder=_delta_zero_conclusion,
    )


def expand_delta_zero_from_suspension_iso(goal):
    if not isinstance(goal, TodaDeltaZeroStatement):
        return ()
    delta = goal.map
    if not isinstance(delta, TodaDeltaMap):
        return ()
    source, middle = delta.source_group, delta.target_group
    q, n = middle.group_dimension, middle.sphere_dimension
    if type(q) is not int or type(n) is not int or n < 1 or q < n:
        return ()
    suspension = TodaSuspensionMap(
        source_group=middle,
        target_group=TodaPrimaryGroup(q + 1, n + 1),
    )
    exactness = TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
            source_term=source,
            middle_term=middle,
            target_term=suspension.target_group,
            first_map=EHP_DELTA_MAP,
            second_map=EHP_E_MAP,
        )
    )
    return (GoalExpansion(
        delta_zero_from_suspension_iso_and_exactness_rule(),
        (TodaSuspensionIsomorphismStatement(map=suspension), exactness),
    ),)


def audit_delta_pi32():
    delta = TodaDeltaZeroStatement(
        TodaDeltaMap(TodaPrimaryGroup(3,3),TodaPrimaryGroup(1,1))
    )
    expansions = expand_delta_zero_from_suspension_iso(delta)
    return {
        "phase": "165 R14-R11",
        "delta_goal": repr(delta),
        "expansions": len(expansions),
        "required_subgoals": [repr(x) for x in expansions[0].subgoals] if expansions else [],
        "e_pi11_pi22_iso_certified": False,
        "prop42_exactness_certified": False,
        "new_certified_leaves": 0,
        "toda_proof_steps_created": 0,
        "status": "DELTA_ZERO_DERIVATION_WIRED_PREMISES_UNCERTIFIED",
        "full_pytest_run": False,
    }
