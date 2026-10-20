"""Rewrite an already transported one-suspension cyclic generator using proof evidence."""
from __future__ import annotations

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, Relation, RelationType


def generator_transport_normalization_rule():
    """Transported finite cyclic relation + proved generator suspension -> named relation."""
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
        return (
            transported.lhs == witness.map.target_group
            and isinstance(suspended, IteratedSuspension)
            and suspended.exponent == 1
            and suspended.expression == witness.source_generator
        )

    def conclusion(premises):
        transported, witness = (step.conclusion for step in premises)
        return Relation(
            transported.lhs,
            FiniteCyclicGroup(transported.rhs.order, witness.target_generator),
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


def expand_generator_transport_normalization(goal: object):
    """A backward step must prove both transport and generator-image evidence."""
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and isinstance(goal.lhs, TodaPrimaryGroup)
        and isinstance(goal.rhs, FiniteCyclicGroup)
    ):
        return ()
    n = goal.lhs.sphere_dimension
    if type(n) is not int or n < 3 or goal.lhs.group_dimension != n + 1:
        return ()

    # This existing library supplies a goal for an η-family generator suspension.
    # Other families require their own *proved* suspension witness, not guessing.
    from toda_rules import toda_eta_family_definition_statement
    from phase165_r12_r21_eta_generator_chain import _eta_pair
    if goal.rhs.generator != toda_eta_family_definition_statement(n).element:
        return ()
    source_group = TodaPrimaryGroup(n, n - 1)
    source = toda_eta_family_definition_statement(n - 1).element
    witness = GeneratorSuspension(
        TodaSuspensionMap(source_group, goal.lhs), source, goal.rhs.generator,
    )
    if _eta_pair(witness) is None:
        return ()
    transported = Relation(
        goal.lhs, FiniteCyclicGroup(goal.rhs.order, IteratedSuspension(source, 1)),
        RelationType.EQUALITY,
    )
    return (GoalExpansion(generator_transport_normalization_rule(), (transported, witness)),)
