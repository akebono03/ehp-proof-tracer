"""Resolve the citing assertion for a concrete goal specialized from a fixed eta claim."""
from __future__ import annotations

from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    specialize_eta_group_relation,
)
from proof import Relation
from unified_statement_registry import AssertionOrigin


def resolve_specialized_goal_citing_id(bridge, goal: Relation) -> str | None:
    """Resolve a unique citation boundary from registered goal statements.

    Exact registered goals take precedence. For a generic assertion, its own
    specialization rule decides whether the requested instance is valid.
    """
    if not isinstance(goal, Relation):
        return None

    exact_matches = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if ":component:" in assertion.assertion_id:
            continue
        if assertion.content != goal:
            continue
        if assertion.component_position is None:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None:
            continue
        exact_matches.append(assertion.assertion_id)

    if exact_matches:
        return exact_matches[0] if len(exact_matches) == 1 else None

    sphere_dimension = getattr(goal.lhs, "sphere_dimension", None)
    matches = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if ":component:" in assertion.assertion_id:
            continue
        if not _is_generic_eta_group_relation(assertion.content):
            continue
        if assertion.component_position is None:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None:
            continue
        try:
            specialized = specialize_eta_group_relation(
                assertion.content, sphere_dimension
            )
        except (ValueError, TypeError):
            continue
        if specialized == goal:
            matches.append(assertion.assertion_id)
    return matches[0] if len(matches) == 1 else None
