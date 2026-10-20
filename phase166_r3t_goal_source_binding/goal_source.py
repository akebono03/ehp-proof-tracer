"""Resolve the citing assertion for a concrete goal specialized from a fixed eta claim."""
from __future__ import annotations

from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    specialize_eta_group_relation,
)
from proof import Relation
from unified_statement_registry import AssertionOrigin


def resolve_specialized_goal_citing_id(bridge, goal: Relation) -> str | None:
    """Use the canonical registered general claim only when its specialization matches.

    A composite parent and its generated component are not alternative publication
    positions. Never invent an assertion or decide ties by insertion order.
    """
    if not isinstance(goal, Relation):
        return None
    n = getattr(goal.lhs, "sphere_dimension", None)
    if isinstance(n, bool) or not isinstance(n, int) or n < 4:
        return None
    matches = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if ":component:" in assertion.assertion_id:
            continue
        if not _is_generic_eta_group_relation(assertion.content):
            continue
        if specialize_eta_group_relation(assertion.content, n) != goal:
            continue
        if assertion.component_position is None:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None:
            continue
        matches.append(assertion.assertion_id)
    return matches[0] if len(matches) == 1 else None
