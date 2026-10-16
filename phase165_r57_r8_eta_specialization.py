"""R57-R8: specialize a cited symbolic eta group statement by an inference.

This module NEVER manufactures a GIVEN proof step or asserts that a goal is true.
The source premise must be admitted by the ordinary citation-screened registry.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass

from expression import GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def _is_generic_eta_group_relation(statement: object) -> bool:
    if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
        return False
    lhs, rhs = statement.lhs, statement.rhs
    if not isinstance(lhs, TodaPrimaryGroup) or not isinstance(rhs, FiniteCyclicGroup):
        return False
    n = lhs.sphere_dimension
    return (
        isinstance(n, ScalarSymbol)
        and isinstance(lhs.group_dimension, ScalarSum)
        and lhs.group_dimension.left == n
        and lhs.group_dimension.right == 1
        and rhs.order == 2
        and isinstance(rhs.generator, HomotopyElement)
        and rhs.generator.dimension == n
        and rhs.generator.target == n
        and isinstance(rhs.generator.source, ScalarSum)
        and rhs.generator.source.left == n
        and rhs.generator.source.right == 1
        and isinstance(rhs.generator.generator, GeneratorSymbol)
        and rhs.generator.generator.family == "η"
        and rhs.generator.generator.index == n
    )


def specialize_eta_group_relation(statement: object, sphere_dimension: int) -> Relation:
    """Produce a candidate specialization; not a proved theorem by itself."""
    if not _is_generic_eta_group_relation(statement):
        raise ValueError("source must be the registered symbolic eta group relation")
    if isinstance(sphere_dimension, bool) or not isinstance(sphere_dimension, int) or sphere_dimension < 4:
        raise ValueError("Toda Proposition 5.1 higher-eta range requires n >= 4")
    n = sphere_dimension
    original = statement.rhs.generator
    eta = HomotopyElement(
        name="η_" + str(n), dimension=n, source=n + 1, target=n,
        generator=GeneratorSymbol(family="η", index=n),
    )
    return Relation(
        lhs=TodaPrimaryGroup(group_dimension=n + 1, sphere_dimension=n),
        rhs=FiniteCyclicGroup(order=statement.rhs.order, generator=eta),
        relation_type=RelationType.EQUALITY,
    )


def _fixed_typed_relations(bridge: object) -> tuple[Relation, ...]:
    """Find general clauses; do not treat archived source text as a statement."""
    registry = getattr(bridge, "registry", bridge)
    assertions = getattr(registry, "_assertions", None)
    if not isinstance(assertions, dict):
        raise TypeError("expected Unified Statement Registry or RegistryBridgeResult")
    found = []
    def visit(content):
        if isinstance(content, Relation):
            if _is_generic_eta_group_relation(content) and content not in found:
                found.append(content)
            return
        if is_dataclass(content) and not isinstance(content, type):
            for field in fields(content):
                visit(getattr(content, field.name))
    for assertion in assertions.values():
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            visit(assertion.content)
    return tuple(found)


def specialized_eta_group_goal_candidates(group: TodaPrimaryGroup, bridge: object) -> tuple[Relation, ...]:
    """Return proposed goals only, without marking them proved or sourcing GIVEN."""
    if not isinstance(group, TodaPrimaryGroup):
        raise TypeError("group must be TodaPrimaryGroup")
    n = group.sphere_dimension
    if isinstance(n, bool) or not isinstance(n, int) or n < 4 or group.group_dimension != n + 1:
        return ()
    return tuple(
        candidate for statement in _fixed_typed_relations(bridge)
        if (candidate := specialize_eta_group_relation(statement, n)).lhs == group
    )


def eta_specialization_inference_rule(goal: Relation) -> InferenceRule:
    """Check the cited general premise again when constructing the ProofStep."""
    if not isinstance(goal, Relation) or not isinstance(goal.lhs, TodaPrimaryGroup):
        raise TypeError("a concrete group relation goal is required")
    n = goal.lhs.sphere_dimension
    def guard(premises, bindings):
        if len(premises) != 1:
            return False
        source = premises[0].conclusion
        return _is_generic_eta_group_relation(source) and specialize_eta_group_relation(source, n) == goal
    def build_conclusion(premises):
        return specialize_eta_group_relation(premises[0].conclusion, n)
    return InferenceRule(
        name="Toda Proposition 5.1 generic higher-eta specialization",
        description="Instantiate n >= 4 in a registered symbolic higher-eta group statement.",
        premise_patterns=(PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),),
        conclusion_builder=build_conclusion,
        match_guard=guard,
    )


def expand_registered_eta_specialization(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Use screened typed ProofStep conclusions, not unscreened catalog entries."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(goal, Relation) or not isinstance(goal.lhs, TodaPrimaryGroup):
        return ()
    n = goal.lhs.sphere_dimension
    if isinstance(n, bool) or not isinstance(n, int) or n < 4:
        return ()
    sources = tuple(source for source in available
                    if _is_generic_eta_group_relation(source)
                    and specialize_eta_group_relation(source, n) == goal)
    return tuple(GoalExpansion(eta_specialization_inference_rule(goal), (source,))
                 for source in sources)
