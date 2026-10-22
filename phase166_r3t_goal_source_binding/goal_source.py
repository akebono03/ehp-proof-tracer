"""Resolve citation boundaries for concrete group goals by their dimensions."""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    specialize_eta_group_relation,
)
from proof import Relation, RelationType
from unified_statement_registry import AssertionOrigin


_GROUP_STRUCTURES = (DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup)


def _same_group_structure(goal: Relation, assertion_relation: Relation) -> bool:
    """Compare concrete group presentations without inferring new equalities.

    Prefer exact equality; otherwise use the registered HyoujiGen identities
    only for the supported, fully resolved generator factors.
    """
    if goal == assertion_relation:
        return True
    a = goal.rhs
    b = assertion_relation.rhs
    if type(a) is not type(b):
        return False
    if isinstance(a, FiniteCyclicGroup) and a.order != b.order:
        return False
    if isinstance(a, FiniteCyclicGroup) and a.generator == b.generator:
        return True
    if isinstance(a, FreeCyclicGroup) and a.generator == b.generator:
        return True
    if isinstance(a, DirectSumGroup) and a == b:
        return True
    from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
    return same_registered_group_presentation(a, b)


def resolve_specialized_goal_citing_id(bridge, goal: Relation) -> str | None:
    """Find a unique, positioned literature claim for the group's typed goal.

    Candidate selection is dimension-first. Content must also match; a claim
    mentioning the same group but asserting something else is not a boundary.
    Generic eta claims use their existing checked specialization mechanism.
    A source with missing position, or competing matches, is not guessed.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, TodaPrimaryGroup)
            or not isinstance(goal.rhs, _GROUP_STRUCTURES)):
        return None
    n = goal.lhs.sphere_dimension
    m = goal.lhs.group_dimension
    if not isinstance(n, int) or not isinstance(m, int):
        return None

    concrete = []
    generic = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if ":component:" in assertion.assertion_id:
            continue
        if assertion.component_position is None:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None:
            continue
        statement = assertion.content
        if not isinstance(statement, Relation):
            continue
        if (statement.relation_type is RelationType.EQUALITY
                and isinstance(statement.lhs, TodaPrimaryGroup)
                and statement.lhs.group_dimension == m
                and statement.lhs.sphere_dimension == n
                and isinstance(statement.rhs, _GROUP_STRUCTURES)
                and _same_group_structure(goal, statement)):
            concrete.append(assertion.assertion_id)
            continue
        if not _is_generic_eta_group_relation(statement):
            continue
        try:
            specialized = specialize_eta_group_relation(statement, n)
        except (ValueError, TypeError):
            continue
        if specialized == goal:
            generic.append(assertion.assertion_id)
    if concrete:
        return concrete[0] if len(concrete) == 1 else None
    return generic[0] if len(generic) == 1 else None
