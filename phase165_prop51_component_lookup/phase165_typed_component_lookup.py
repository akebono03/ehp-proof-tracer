"""Index typed components of composite registered assertions without citation promotion.

A component is a searchable view of its parent assertion, not a new source
assertion and not an independently approved GIVEN proof step.
"""
from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from typing import Callable

from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


@dataclass(frozen=True)
class TypedComponentMatch:
    assertion_id: str
    reference_id: str
    component_name: str
    content: object
    origin: AssertionOrigin



def index_typed_components(registry: UnifiedStatementRegistry) -> tuple[TypedComponentMatch, ...]:
    """Create a lossless read-only index of fixed typed assertions and their fields."""
    if not isinstance(registry, UnifiedStatementRegistry):
        raise TypeError("registry must be UnifiedStatementRegistry")
    matches = []
    for assertion in registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        value = assertion.content
        if (is_dataclass(value) and not isinstance(value, type)
                and type(value).__name__ in ("TodaProp51FiniteDimensionalStatement", "CompositeFact")):
            components = tuple((field.name, getattr(value, field.name)) for field in fields(value))
        else:
            components = (("__self__", value),)
        for name, content in components:
            if content is None:
                continue
            matches.append(TypedComponentMatch(
                assertion_id=assertion.assertion_id,
                reference_id=assertion.reference_id,
                component_name=name,
                content=content,
                origin=assertion.origin,
            ))
    return tuple(matches)



def search_typed_components(
    registry: UnifiedStatementRegistry,
    *,
    reference_locator: str | None = None,
    component_name: str | None = None,
    predicate: Callable[[object], bool] | None = None,
) -> tuple[TypedComponentMatch, ...]:
    """Find individual typed components without creating proof steps or citations."""
    if predicate is not None and not callable(predicate):
        raise TypeError("predicate must be callable")
    results = []
    for match in index_typed_components(registry):
        if component_name is not None and match.component_name != component_name:
            continue
        if reference_locator is not None:
            reference = registry._references[match.reference_id]
            if reference.locator != reference_locator:
                continue
        if predicate is not None and not predicate(match.content):
            continue
        results.append(match)
    return tuple(results)
