"""Backward transport along the cited Toda (5.2) eta_2 composition isomorphism.

This module proposes proof subgoals; it never supplies a group relation as GIVEN.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from proof import InferenceRule, LiteratureReference, PremisePattern, Relation, RelationType


def _eta2_composition_parts(generator: object):
    if not isinstance(generator, Composition):
        return None
    left, right = generator.left, generator.right
    if not isinstance(left, HomotopyElement) or not isinstance(right, HomotopyElement):
        return None
    if (left.dimension != 2 or left.source != 3 or left.target != 2
            or left.generator != GeneratorSymbol(family="η", index=2)):
        return None
    if (right.dimension != 3 or right.source != 4 or right.target != 3
            or right.generator != GeneratorSymbol(family="η", index=3)):
        return None
    return right


def _toda52_rule(expected: Relation) -> InferenceRule:
    def guard(premises, bindings):
        if len(premises) != 2:
            return False
        source, theorem = (step.conclusion for step in premises)
        if not isinstance(theorem, Toda52UniversalStatement):
            return False
        if (theorem.minimum_i != 3 or theorem.variable != "i"
                or theorem.map_formula != "alpha -> eta_2 o alpha"
                or theorem.source_group != "pi_i^3" or theorem.target_group != "pi_i^2"):
            return False
        if (not isinstance(source, Relation)
                or source.relation_type is not RelationType.EQUALITY
                or source.lhs != TodaPrimaryGroup(4, 3)
                or not isinstance(source.rhs, FiniteCyclicGroup)
                or source.rhs.order != 2):
            return False
        parts = _eta2_composition_parts(expected.rhs.generator)
        if parts is None:
            return False
        eta3 = source.rhs.generator
        return (isinstance(eta3, HomotopyElement)
                and eta3.dimension == parts.dimension
                and eta3.source == parts.source
                and eta3.target == parts.target
                and eta3.generator == parts.generator
                and expected.lhs == TodaPrimaryGroup(4, 2))

    def conclusion(premises):
        return expected

    return InferenceRule(
        name="Toda (5.2) finite-cyclic eta2 composition transport",
        description="Transport a proved cyclic structure along the cited (5.2) isomorphism at i=4.",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=Toda52UniversalStatement),
        ),
        conclusion_builder=conclusion,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda (5.2)", locator="(5.2)",
        ),
    )


def expand_toda52_finite_cyclic_goal(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Offer a verified two-premise path only if (5.2) survived citation screening."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not (isinstance(goal, Relation) and goal.relation_type is RelationType.EQUALITY
            and goal.lhs == TodaPrimaryGroup(4, 2)
            and isinstance(goal.rhs, FiniteCyclicGroup)
            and goal.rhs.order == 2):
        return ()
    eta3 = _eta2_composition_parts(goal.rhs.generator)
    if eta3 is None:
        return ()
    source = Relation(
        lhs=TodaPrimaryGroup(4, 3),
        rhs=FiniteCyclicGroup(
            order=2,
            generator=HomotopyElement(
                name="η_3", dimension=eta3.dimension,
                source=eta3.source, target=eta3.target,
                generator=eta3.generator,
            ),
        ),
        relation_type=RelationType.EQUALITY,
    )
    accepted = tuple(item for item in available if isinstance(item, Toda52UniversalStatement)
                     and item.minimum_i == 3
                     and item.map_formula == "alpha -> eta_2 o alpha"
                     and item.source_group == "pi_i^3"
                     and item.target_group == "pi_i^2"
                     and item.variable == "i")
    return tuple(GoalExpansion(_toda52_rule(goal), (source, item)) for item in accepted)
