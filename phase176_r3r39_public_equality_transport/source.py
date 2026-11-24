"""Public backward plan for the six existing right-Hopf equality steps.

This registers no mathematical rule. Every node is a regular GoalExpansion
whose rule is one of the pre-existing equality/Hopf congruence rules.
The two input leaves remain independent proof-search obligations.
"""
from __future__ import annotations

from collections.abc import Callable

from expression import Composition, MapApplication, Suspension
from hopf_rules import ehp_h_preserves_equality_inference_rule
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r34_composite_suspension_isolated.source import (
    composite_suspension_equality_input,
)
from phase176_r3r38_equality_transport_isolated.source import (
    right_hopf_transport_inputs,
)
from proof import Relation, RelationType
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)


def right_hopf_transport_backward_plan(
    goal: object,
    available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Produce exact six ordinary inference nodes, without proving a leaf.

    The finite candidate beta = delta o gamma.left is merely a backward-search
    hypothesis. The ordinary suspension-image derivation must establish
    E(beta) = gamma; no inverse suspension equality is assumed. This choice
    is structural, not tied to eta/nu names or a particular group query.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)
            or not isinstance(goal.rhs.right, Composition)
            or goal.lhs.expression.right != goal.rhs.right):
        return ()

    alpha = goal.lhs.expression.left
    delta = goal.rhs.left
    gamma = goal.rhs.right
    beta = Composition(delta, gamma.left)
    inputs = right_hopf_transport_inputs(goal, beta)
    if inputs is None:
        return ()
    substituted, suspension = inputs
    if composite_suspension_equality_input(suspension) is None:
        return ()

    hopf_value = Relation(
        MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY,
    )
    if (available.count(TodaProp22RightFormula()) != 1
            or available.count(hopf_value) != 1):
        return ()

    suspended = Suspension(beta)
    alpha_composition = Relation(
        Composition(alpha, suspended), Composition(alpha, gamma),
        RelationType.EQUALITY,
    )
    hopf_composition = Relation(
        substituted.lhs, goal.lhs, RelationType.EQUALITY,
    )
    reversed_hopf_composition = Relation(
        goal.lhs, substituted.lhs, RelationType.EQUALITY,
    )
    delta_composition = Relation(
        substituted.rhs, goal.rhs, RelationType.EQUALITY,
    )
    intermediate = Relation(
        goal.lhs, substituted.rhs, RelationType.EQUALITY,
    )
    return (
        (alpha_composition, GoalExpansion(
            equality_preserved_under_left_composition_inference_rule(alpha),
            (suspension,),
        )),
        (hopf_composition, GoalExpansion(
            ehp_h_preserves_equality_inference_rule(),
            (alpha_composition,),
        )),
        (reversed_hopf_composition, GoalExpansion(
            equality_symmetry_inference_rule(),
            (hopf_composition,),
        )),
        (delta_composition, GoalExpansion(
            equality_preserved_under_left_composition_inference_rule(delta),
            (suspension,),
        )),
        (intermediate, GoalExpansion(
            equality_transitivity_inference_rule(),
            (reversed_hopf_composition, substituted),
        )),
        (goal, GoalExpansion(
            equality_transitivity_inference_rule(),
            (intermediate, delta_composition),
        )),
    )


def build_public_right_hopf_transport_provider(
    available: tuple[object, ...],
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Retain the exact intermediate stages within one source-screened DFS.

    A stage is cached only after its parent has been proposed. This avoids
    introducing global assumptions, pre-completed proofs, or out-of-context
    equality candidates. DFS must independently replay each of the six nodes.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    stages: dict[Relation, GoalExpansion] = {}

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if not isinstance(goal, Relation):
            return ()
        if goal in stages:
            return (stages[goal],)
        plan = right_hopf_transport_backward_plan(goal, available)
        if not plan:
            return ()
        # Two different goals must not inject conflicting backward steps.
        if any(target in stages for target, _proposal in plan):
            return ()
        stages.update(plan)
        return (stages[goal],)

    return expand
