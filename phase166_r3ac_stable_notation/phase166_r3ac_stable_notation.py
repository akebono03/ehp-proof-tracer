"""Normalize the cited stable eta-family notation after generic Toda (4.5) transport.

The transported group is derived independently. This rule only identifies its
iterated-suspension generator with the adopted eta-family notation.
"""
from __future__ import annotations

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, Relation, RelationType
from toda_rules import toda_eta_family_definition_statement


def _stable_eta_renaming_shape(transported: object, goal: object) -> bool:
    if not (isinstance(transported, Relation) and isinstance(goal, Relation)
            and transported.relation_type is RelationType.EQUALITY
            and goal.relation_type is RelationType.EQUALITY
            and transported.lhs == goal.lhs
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(transported.rhs, FiniteCyclicGroup)
            and isinstance(goal.rhs, FiniteCyclicGroup)
            and transported.rhs.order == goal.rhs.order):
        return False
    suspended = transported.rhs.generator
    if not isinstance(suspended, IteratedSuspension):
        return False
    r = suspended.exponent
    if type(r) is not int or r < 2:
        return False
    source = suspended.expression
    from expression import HomotopyElement
    if not isinstance(source, HomotopyElement):
        return False
    source_n = source.target
    if type(source_n) is not int or source_n < 2:
        return False
    target_n = source_n + r
    if (goal.lhs != TodaPrimaryGroup(target_n + 1, target_n)
            or source != toda_eta_family_definition_statement(source_n).element):
        # An alias of the same eta symbol is allowed only when its full typed
        # generator data agrees; the textual name is not mathematical evidence.
        from phase165_r12_r28_presentation_connection import _matching_eta_name
        canonical = toda_eta_family_definition_statement(source_n).element
        if not _matching_eta_name(source, canonical):
            return False
        if (source.dimension != canonical.dimension or source.source != canonical.source
                or source.target != canonical.target or source.generator != canonical.generator
                or goal.lhs != TodaPrimaryGroup(target_n + 1, target_n)):
            return False
    expected = toda_eta_family_definition_statement(target_n).element
    from phase165_r12_r28_presentation_connection import _matching_eta_name
    result = goal.rhs.generator
    return (_matching_eta_name(result, expected)
            and getattr(result, 'dimension', None) == expected.dimension
            and getattr(result, 'source', None) == expected.source
            and getattr(result, 'target', None) == expected.target
            and getattr(result, 'generator', None) == expected.generator)


def stable_eta_notation_rule(goal: Relation) -> InferenceRule:
    """Require a transported relation and the cited general eta definition."""
    def guard(premises, bindings):
        return (len(premises) == 2
                and premises[1].conclusion == TodaEtaFamilyGeneralDefinition()
                and _stable_eta_renaming_shape(premises[0].conclusion, goal))

    return InferenceRule(
        name='cited stable eta-family notation for iterated transport',
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=TodaEtaFamilyGeneralDefinition),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_stable_eta_notation(goal: object, available: tuple[object, ...]):
    """Find earlier cited group structures; never posit their truth."""
    if not isinstance(available, tuple):
        raise TypeError('available must be tuple')
    if available.count(TodaEtaFamilyGeneralDefinition()) != 1:
        return ()
    if not (isinstance(goal, Relation) and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(goal.rhs, FiniteCyclicGroup)):
        return ()
    results = []
    for source in available:
        if not (isinstance(source, Relation) and isinstance(source.lhs, TodaPrimaryGroup)
                and isinstance(source.rhs, FiniteCyclicGroup)
                and source.relation_type is RelationType.EQUALITY):
            continue
        n, m = source.lhs.sphere_dimension, goal.lhs.sphere_dimension
        if type(n) is not int or type(m) is not int or m - n < 2:
            continue
        if source.lhs.group_dimension - n != goal.lhs.group_dimension - m:
            continue
        transported = Relation(
            goal.lhs,
            FiniteCyclicGroup(source.rhs.order, IteratedSuspension(source.rhs.generator, m - n)),
            RelationType.EQUALITY,
        )
        if not _stable_eta_renaming_shape(transported, goal):
            continue
        option = GoalExpansion(stable_eta_notation_rule(goal),
                               (transported, TodaEtaFamilyGeneralDefinition()))
        if all(existing.subgoals != option.subgoals for existing in results):
            results.append(option)
    return tuple(results)
