"""Goal-driven EHP exactness obligations; never create GIVEN references."""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r14_r26_prop42_typed import typed_delta_e_window
from proof import Relation, RelationType
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class GoalExactnessObligations:
    goal: Relation
    delta_e: TodaProp42ExactnessStatement
    e_h: TodaProp42ExactnessStatement
    prop42_n: int
    prop42_i: int


def goal_exactness_obligations(goal: Relation) -> GoalExactnessObligations:
    """Construct only the two consecutive EHP windows adjacent to a group goal.

    This is type-safe index arithmetic, NOT a proof of either exactness statement.
    The returned statements remain subgoals pending source instantiation and
    strict citation checks. Neither the goal's right-hand structure nor its
    generator is used as a proved assumption.
    """
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        raise TypeError("expected a group-structure equality goal")
    group = goal.lhs
    if not isinstance(group, TodaPrimaryGroup):
        raise TypeError("goal lhs must be TodaPrimaryGroup")
    q, s = group.group_dimension, group.sphere_dimension
    if type(q) is not int or type(s) is not int or s < 2 or q < s:
        raise ValueError("EHP goal must have concrete dimensions q >= s >= 2")
    n, i = s - 1, q
    delta_e = typed_delta_e_window(n, i)
    if delta_e.window.target_term != group:
        raise ValueError("Proposition 4.2 specialization does not reach the goal")
    e_h = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(q - 1, s - 1),
        middle_term=group,
        target_term=TodaPrimaryGroup(q, 2 * s - 1),
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))
    if delta_e.window.middle_term != e_h.window.source_term:
        raise ValueError("EHP windows do not share the suspension source")
    return GoalExactnessObligations(goal, delta_e, e_h, n, i)


def exactness_goals_in_context(obligations: GoalExactnessObligations, bridge: object) -> dict:
    """Check exact typed statements in admitted GIVEN links; do not create leaves.

    A link may only discharge an exactness goal after an independent citation
    gate has screened the bridge. This helper intentionally cannot assert that
    the bridge was screened: the caller must supply that provenance.
    """
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    found = {"delta_e": [], "e_h": []}
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN or step.premises:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is not type(step.conclusion) or assertion.content != step.conclusion:
            continue
        for label, required in (("delta_e", obligations.delta_e), ("e_h", obligations.e_h)):
            if step.conclusion == required:
                found[label].append(link.assertion_id)
    return {name: tuple(ids) for name, ids in found.items()}
