"""Evidence-bound eta-name adaptation for finite cyclic Toda transport.

ASCII-underscore and Unicode-subscript spellings of the same typed eta
are not mathematical premises. Suspension and transport remain proof subgoals.
"""
from __future__ import annotations

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, Relation, RelationType
from phase165_r12_r28_presentation_connection import _matching_eta_name


def generator_transport_normalization_rule(goal: Relation | None = None):
    """A proved suspension identifies the named cyclic generator after transport."""
    def guard(premises, bindings):
        if len(premises) != 2:
            return False
        transported, witness = (step.conclusion for step in premises)
        if not isinstance(transported, Relation) or not isinstance(witness, GeneratorSuspension):
            return False
        if transported.relation_type is not RelationType.EQUALITY:
            return False
        if not isinstance(transported.rhs, FiniteCyclicGroup):
            return False
        if not isinstance(witness.map, TodaSuspensionMap):
            return False
        suspended = transported.rhs.generator
        if not (
            transported.lhs == witness.map.target_group
            and isinstance(suspended, IteratedSuspension)
            and suspended.exponent == 1
            and _matching_eta_name(suspended.expression, witness.source_generator)
        ):
            return False
        if goal is None:
            return True
        return (
            isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and goal.lhs == transported.lhs
            and isinstance(goal.rhs, FiniteCyclicGroup)
            and goal.rhs.order == transported.rhs.order
            and _matching_eta_name(goal.rhs.generator, witness.target_generator)
        )

    def conclusion(premises):
        transported, witness = (step.conclusion for step in premises)
        generator = witness.target_generator if goal is None else goal.rhs.generator
        return Relation(
            transported.lhs,
            FiniteCyclicGroup(transported.rhs.order, generator),
            RelationType.EQUALITY,
        )

    return InferenceRule(
        name="proved generator suspension normalizes transported cyclic group",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=GeneratorSuspension),
        ),
        match_guard=guard,
        conclusion_builder=conclusion,
    )


def expand_generator_transport_normalization(
    goal: object, available: tuple[object, ...] = (),
) -> tuple[GoalExpansion, ...]:
    """Bind transported generator to actual earlier groups in screened context."""
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and isinstance(goal.lhs, TodaPrimaryGroup)
        and isinstance(goal.rhs, FiniteCyclicGroup)
    ):
        return ()
    if not isinstance(available, tuple):
        raise TypeError("available must be tuple")
    n = goal.lhs.sphere_dimension
    if type(n) is not int or n < 4 or goal.lhs.group_dimension != n + 1:
        return ()

    from toda_rules import toda_eta_family_definition_statement
    from phase165_r12_r21_eta_generator_chain import _eta_pair
    canonical_target = toda_eta_family_definition_statement(n).element
    if not _matching_eta_name(goal.rhs.generator, canonical_target):
        return ()
    source_group = TodaPrimaryGroup(n, n - 1)
    canonical_source = toda_eta_family_definition_statement(n - 1).element
    witness = GeneratorSuspension(
        TodaSuspensionMap(source_group, goal.lhs), canonical_source, canonical_target,
    )
    if _eta_pair(witness) is None:
        return ()

    earlier = tuple(
        item.rhs.generator for item in available
        if isinstance(item, Relation)
        and item.relation_type is RelationType.EQUALITY
        and item.lhs == source_group
        and isinstance(item.rhs, FiniteCyclicGroup)
        and item.rhs.order == goal.rhs.order
        and _matching_eta_name(item.rhs.generator, canonical_source)
    )
    # Retain the existing no-context API for existing focused tests. In the
    # actual screened search use only generators from cited earlier groups.
    if not available:
        earlier = (canonical_source,)
    results = []
    for source in earlier:
        transported = Relation(
            goal.lhs,
            FiniteCyclicGroup(goal.rhs.order, IteratedSuspension(source, 1)),
            RelationType.EQUALITY,
        )
        candidate = GoalExpansion(generator_transport_normalization_rule(goal), (transported, witness))
        if all(item.subgoals != candidate.subgoals for item in results):
            results.append(candidate)
    return tuple(results)
