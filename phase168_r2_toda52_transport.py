"""Backward transport along the cited Toda (5.2) eta_2 composition isomorphism.

Every proposed transport needs a separately screened source group proof and
Toda (5.2). Neither DB goals nor generator names are accepted as GIVEN facts.
The established i=4 proposal is retained unchanged.
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


def _toda52_theorem_is_exact(item: object) -> bool:
    return (isinstance(item, Toda52UniversalStatement)
            and item.minimum_i == 3
            and item.map_formula == "alpha -> eta_2 o alpha"
            and item.source_group == "pi_i^3"
            and item.target_group == "pi_i^2"
            and item.variable == "i")


def _typed_source_and_target(expression: object) -> tuple[int, int] | None:
    """Check concrete composite types without guessing from printed names."""
    if isinstance(expression, HomotopyElement):
        if (type(expression.source) is int and type(expression.target) is int
                and expression.source > expression.target >= 2):
            return expression.source, expression.target
        return None
    if isinstance(expression, Composition):
        left = _typed_source_and_target(expression.left)
        right = _typed_source_and_target(expression.right)
        if left is None or right is None or right[1] != left[0]:
            return None
        return right[0], left[1]
    return None


def _eta2_right_generator(goal: Relation) -> object | None:
    """Return a typed map S^m -> S^3 whose eta_2 composition is the target."""
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        return None
    candidate = goal.rhs.generator
    if not isinstance(candidate, Composition):
        return None
    eta2 = candidate.left
    if (not isinstance(eta2, HomotopyElement)
            or type(eta2.dimension) is not int
            or eta2.dimension != 2 or eta2.source != 3 or eta2.target != 2
            or eta2.generator != GeneratorSymbol(family="η", index=2)):
        return None
    right = candidate.right
    if _typed_source_and_target(right) != (goal.lhs.group_dimension, 3):
        return None
    return right


def _toda52_general_rule(expected: Relation, source: Relation) -> InferenceRule:
    """Use only a screened, exact source and the cited universal theorem."""
    if (not isinstance(expected, Relation) or not isinstance(source, Relation)
            or expected.relation_type is not RelationType.EQUALITY
            or source.relation_type is not RelationType.EQUALITY
            or not isinstance(expected.rhs, FiniteCyclicGroup)
            or not isinstance(source.rhs, FiniteCyclicGroup)
            or expected.rhs.order != source.rhs.order
            or expected.lhs.sphere_dimension != 2
            or source.lhs != TodaPrimaryGroup(expected.lhs.group_dimension, 3)):
        raise ValueError("invalid (5.2) transport source or target")

    def guard(premises, bindings):
        if len(premises) != 2:
            return False
        first, second = (step.conclusion for step in premises)
        if first != source or not _toda52_theorem_is_exact(second):
            return False
        right = _eta2_right_generator(expected)
        if right is None:
            return False
        from phase168_r2_8_3_generator_identity.identity import (
            same_registered_group_presentation,
        )
        typed_right = FiniteCyclicGroup(order=expected.rhs.order, generator=right)
        return (typed_right == source.rhs
                or same_registered_group_presentation(typed_right, source.rhs))

    return InferenceRule(
        name="Toda (5.2) typed finite-cyclic composition transport",
        description="Transport a separately proved cyclic group along the cited (5.2) isomorphism.",
        premise_patterns=(
            PremisePattern(statement_type=Relation, statement_pattern=source),
            PremisePattern(statement_type=Toda52UniversalStatement),
        ),
        conclusion_builder=lambda premises: expected,
        match_guard=guard,
        literature_reference=LiteratureReference(label="Toda (5.2)", locator="(5.2)"),
    )


def expand_toda52_finite_cyclic_goal(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Screened (5.2) finite-cyclic transport at every well-typed m>=4.

    i=4 retains its original route. New m>=5 proposals require an exact,
    separately screened prior Relation for pi_m^3; a DB result is never a leaf.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and type(goal.lhs.group_dimension) is int
            and goal.lhs.sphere_dimension == 2
            and goal.lhs.group_dimension >= 4
            and isinstance(goal.rhs, FiniteCyclicGroup)
            and type(goal.rhs.order) is int
            and goal.rhs.order >= 2):
        return ()
    accepted = tuple(item for item in available if _toda52_theorem_is_exact(item))
    if not accepted:
        return ()
    m = goal.lhs.group_dimension
    if m == 4:
        if goal.rhs.order != 2:
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
        return tuple(GoalExpansion(_toda52_rule(goal), (source, item)) for item in accepted)

    right = _eta2_right_generator(goal)
    if right is None:
        return ()
    from phase168_r2_8_3_generator_identity.identity import (
        same_registered_group_presentation,
    )
    target_source = TodaPrimaryGroup(m, 3)
    right_presentation = FiniteCyclicGroup(order=goal.rhs.order, generator=right)
    sources = []
    for item in available:
        if (not isinstance(item, Relation)
                or item.relation_type is not RelationType.EQUALITY
                or item.lhs != target_source
                or not isinstance(item.rhs, FiniteCyclicGroup)
                or item.rhs.order != goal.rhs.order):
            continue
        if (item.rhs != right_presentation
                and not same_registered_group_presentation(item.rhs, right_presentation)):
            continue
        if item not in sources:
            sources.append(item)
    return tuple(
        GoalExpansion(_toda52_general_rule(goal, source), (source, theorem))
        for source in sources
        for theorem in accepted
    )
