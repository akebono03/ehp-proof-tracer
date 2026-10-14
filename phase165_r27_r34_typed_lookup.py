"""Typed generator/operation lookup via the common backward prover.

A matched source assertion is a goal, not evidence. Only a successful
reconstruction counts as a proven result. No legacy ProofRepository is built.
"""
from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum

from expression import GeneratorSymbol, MapApplication
from generator_input import resolve_generator_input
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r9_production_wiring import discover_goal_search_inputs
from proof import Relation, ProofStep
from toda_operation_query import (
    RepositoryCompositionQuery,
    RepositoryGeneratorQuery,
    RepositoryMapOperationQuery,
    RepositoryThreeTermCompositionQuery,
    parse_repository_operation_query,
)
from unified_statement_registry import AssertionOrigin


class TypedLookupStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    SEARCH_FAILED = "search_failed"


@dataclass(frozen=True)
class TypedLookupResult:
    status: TypedLookupStatus
    proven_steps: tuple[ProofStep, ...]
    open_goals: tuple[object, ...]
    diagnostics: tuple[str, ...]


def _walk(value: object, seen: set[int]):
    if id(value) in seen:
        return
    seen.add(id(value))
    yield value
    if is_dataclass(value) and not isinstance(value, type):
        for item in fields(value):
            yield from _walk(getattr(value, item.name), seen)
    elif isinstance(value, (tuple, list, frozenset)):
        for item in value:
            yield from _walk(item, seen)


def _has_generator(value: object, symbol: GeneratorSymbol) -> bool:
    return any(item == symbol for item in _walk(value, set()) if isinstance(item, GeneratorSymbol))


def _query_generators(query: object) -> tuple[GeneratorSymbol, ...]:
    if isinstance(query, RepositoryGeneratorQuery):
        return (query.generator,)
    if isinstance(query, RepositoryCompositionQuery):
        return _query_generators(query.left) + _query_generators(query.right)
    if isinstance(query, RepositoryThreeTermCompositionQuery):
        return (_query_generators(query.first) + _query_generators(query.second)
                + _query_generators(query.third))
    if isinstance(query, RepositoryMapOperationQuery):
        return _query_generators(query.operand)
    raise TypeError("unknown typed operation query")


def _operation_matches(statement: object, query: object) -> bool:
    if not isinstance(statement, Relation):
        return False
    if isinstance(query, RepositoryMapOperationQuery):
        lhs = statement.lhs
        if not isinstance(lhs, MapApplication):
            return False
        operation_name = getattr(lhs.map, "name", None)
        if operation_name is None:
            operation_name = str(lhs.map)
        if query.operation == "Delta":
            if "Delta" not in operation_name and "Δ" not in operation_name:
                return False
        elif query.operation not in operation_name:
            return False
    return all(_has_generator(statement, sym) for sym in _query_generators(query))


def search_typed_statement_matches(predicate, *, discovery=None) -> TypedLookupResult:
    """Find eligible typed goals and prove them via reconstruct_registered_goal."""
    if discovery is None:
        discovery = discover_goal_search_inputs()
    bridge = discovery.bridge
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        return TypedLookupResult(TypedLookupStatus.SEARCH_FAILED, (), (),
                                 ("型付き命題が登録されていません",))
    context_id = assertions[0].assertion_id
    goals = []
    for assertion in assertions:
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        statement = assertion.content
        if predicate(statement) and not any(type(previous) is type(statement) and previous == statement for previous in goals):
            goals.append(statement)
    if not goals:
        return TypedLookupResult(TypedLookupStatus.SEARCH_FAILED, (), (),
                                 ("該当する型付き命題が未登録です",))
    steps = []
    unresolved = []
    for goal in goals:
        try:
            step = reconstruct_registered_goal(
                goal, bridge, context_id, discovery.expansion_provider,
                lookup_mode="typed_reference",
            )
        except RegisteredGoalUnresolved:
            unresolved.append(goal)
            continue
        if step.conclusion != goal:
            unresolved.append(goal)
            continue
        if not any(existing.conclusion == step.conclusion for existing in steps):
            steps.append(step)
    status = (TypedLookupStatus.PARTIAL if steps and unresolved else
              TypedLookupStatus.COMPLETE if steps else TypedLookupStatus.SEARCH_FAILED)
    return TypedLookupResult(status, tuple(steps), tuple(unresolved),
                             ("一部の候補命題は証明できていません",) if unresolved else ())


def search_typed_generator_statements(generator_input: str, *, discovery=None) -> TypedLookupResult:
    symbol = resolve_generator_input(generator_input)
    return search_typed_statement_matches(
        lambda statement: _has_generator(statement, symbol), discovery=discovery,
    )


def search_typed_operation_statements(query_input: str, *, discovery=None) -> TypedLookupResult:
    query = parse_repository_operation_query(query_input)
    return search_typed_statement_matches(
        lambda statement: _operation_matches(statement, query), discovery=discovery,
    )
