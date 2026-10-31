"""Generic typed inference of an injected nonzero generator and order four.

A finite cyclic generator is nonzero for order >= 2. Injectivity transports
its nonzeroness. Equality transfers nonzeroness to a double, and a group
of cardinality four with a nonzero double has an element of order four.

These constructors propose typed conclusions only. They do not create GIVEN
leaves or promote a database goal into a theorem.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import MapApplication, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase165_r14_r6_generic_iso import MapInjective
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10e5_composite_generator_image.rule import _endpoints
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


@dataclass(frozen=True)
class NonZeroGroupElement:
    group: TodaPrimaryGroup
    element: object


@dataclass(frozen=True)
class FiniteElementOrder:
    group: TodaPrimaryGroup
    element: object
    order: int


def nonzero_cyclic_generator_image(
    source_group: object, injective: object, image: object,
) -> NonZeroGroupElement | None:
    """Infer E(x) != 0 for a proved finite-cyclic generator x and injective E.

    Typed HyoujiGen identity bridges prior citations with missing endpoint
    annotations, but never confers proof status without the source relation.
    """
    if (
        not isinstance(source_group, Relation)
        or source_group.relation_type is not RelationType.EQUALITY
        or not isinstance(source_group.lhs, TodaPrimaryGroup)
        or not isinstance(source_group.rhs, FiniteCyclicGroup)
        or type(source_group.rhs.order) is not int
        or source_group.rhs.order < 2
        or not isinstance(injective, MapInjective)
        or not isinstance(injective.map, TodaSuspensionMap)
        or injective.map.source_group != source_group.lhs
        or not isinstance(image, MapApplication)
        or image.map != EHP_E_MAP
    ):
        return None
    source, target = _endpoints(image.expression), injective.map.target_group
    if (
        source != (
            source_group.lhs.group_dimension,
            source_group.lhs.sphere_dimension,
        )
        or target != TodaPrimaryGroup(
            source_group.lhs.group_dimension + 1,
            source_group.lhs.sphere_dimension + 1,
        )
    ):
        return None
    exact_generator = source_group.rhs.generator == image.expression
    registered_identity = same_registered_group_presentation(
        source_group.rhs,
        FiniteCyclicGroup(source_group.rhs.order, image.expression),
    )
    if not exact_generator and not registered_identity:
        return None
    return NonZeroGroupElement(target, image)


def injected_generator_nonzero_rule(
    goal: NonZeroGroupElement,
    source_group: Relation,
    injective: MapInjective,
) -> InferenceRule:
    if nonzero_cyclic_generator_image(source_group, injective, goal.element) != goal:
        raise ValueError("source generator, injection and nonzero image do not match")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].rule is ProofRule.INFERENCE
            and premises[0].conclusion == source_group
            and premises[1].conclusion == injective
            and nonzero_cyclic_generator_image(
                premises[0].conclusion, premises[1].conclusion, goal.element,
            ) == goal
        )

    return InferenceRule(
        name="injective map preserves nonzero finite-cyclic generator",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def nonzero_double_from_equality(
    equality: object, nonzero_image: object,
) -> NonZeroGroupElement | None:
    """Use exact typed equality 2*x=E(y), not display-name matching."""
    if (
        not isinstance(equality, Relation)
        or equality.relation_type is not RelationType.EQUALITY
        or not isinstance(equality.lhs, Multiple)
        or type(equality.lhs.coefficient) is not int
        or equality.lhs.coefficient != 2
        or not isinstance(equality.rhs, MapApplication)
        or equality.rhs.map != EHP_E_MAP
        or not isinstance(nonzero_image, NonZeroGroupElement)
        or nonzero_image.element != equality.rhs
        or not isinstance(nonzero_image.group, TodaPrimaryGroup)
        or _endpoints(equality.lhs.expression) != (
            nonzero_image.group.group_dimension,
            nonzero_image.group.sphere_dimension,
        )
    ):
        return None
    return NonZeroGroupElement(nonzero_image.group, equality.lhs)


def inferred_nonzero_double_rule(
    goal: NonZeroGroupElement,
    equality: Relation,
    nonzero_image: NonZeroGroupElement,
) -> InferenceRule:
    if nonzero_double_from_equality(equality, nonzero_image) != goal:
        raise ValueError("nonzero double does not follow from typed equality")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and premises[0].conclusion == equality
            and premises[1].conclusion == nonzero_image
            and nonzero_double_from_equality(
                premises[0].conclusion, premises[1].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="typed equality transfers nonzeroness to double",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=NonZeroGroupElement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def order_four_from_nonzero_double(
    cardinality: object, nonzero_double: object,
) -> FiniteElementOrder | None:
    """Lagrange: order(x) divides four; 2*x != 0 forces order(x)=4."""
    if (
        not isinstance(cardinality, FiniteGroupCardinality)
        or cardinality.order != 4
        or type(cardinality.order) is not int
        or not isinstance(cardinality.group, TodaPrimaryGroup)
        or not isinstance(nonzero_double, NonZeroGroupElement)
        or nonzero_double.group != cardinality.group
        or not isinstance(nonzero_double.element, Multiple)
        or type(nonzero_double.element.coefficient) is not int
        or nonzero_double.element.coefficient != 2
        or _endpoints(nonzero_double.element.expression) != (
            cardinality.group.group_dimension,
            cardinality.group.sphere_dimension,
        )
    ):
        return None
    return FiniteElementOrder(
        cardinality.group, nonzero_double.element.expression, 4,
    )


def inferred_order_four_rule(
    goal: FiniteElementOrder,
    cardinality: FiniteGroupCardinality,
    nonzero_double: NonZeroGroupElement,
) -> InferenceRule:
    if order_four_from_nonzero_double(cardinality, nonzero_double) != goal:
        raise ValueError("order four cannot be concluded without a nonzero double")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and premises[0].conclusion == cardinality
            and premises[1].conclusion == nonzero_double
            and order_four_from_nonzero_double(
                premises[0].conclusion, premises[1].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="finite order-four group and nonzero double imply order-four element",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=FiniteGroupCardinality),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=NonZeroGroupElement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )

def expand_public_order_four_from_nonzero_double(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Propose the existing order-four inference without assuming its premises.

    A finite group of cardinality four and a proved nonzero double imply that
    the doubled element's underlying generator has order four.  Both typed
    premises must still be independently reconstructed by backward search.
    """
    from phase165_r3_recursive_search import GoalExpansion

    if (
        not isinstance(goal, FiniteElementOrder)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or type(goal.order) is not int
        or goal.order != 4
    ):
        return ()
    cardinality = FiniteGroupCardinality(goal.group, 4)
    double_nonzero = NonZeroGroupElement(
        goal.group, Multiple(2, goal.element),
    )
    if order_four_from_nonzero_double(cardinality, double_nonzero) != goal:
        return ()
    return (
        GoalExpansion(
            inferred_order_four_rule(goal, cardinality, double_nonzero),
            (cardinality, double_nonzero),
        ),
    )

def expand_public_injected_generator_nonzero(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose E(generator) != 0 from one earlier finite-cyclic source and injective E.

    The source relation is an eligible, cited GIVEN candidate, not a DB group
    target.  The E-injectivity subgoal must be independently proved as an
    INFERENCE.  No statement or ProofStep is manufactured by this proposer.
    """
    from phase165_r3_recursive_search import GoalExpansion

    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple of screened source statements")
    if (
        not isinstance(goal, NonZeroGroupElement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or not isinstance(goal.element, MapApplication)
        or goal.element.map != EHP_E_MAP
    ):
        return ()
    q = goal.group.group_dimension
    n = goal.group.sphere_dimension
    if (
        type(q) is not int
        or type(n) is not int
        or n < 3
        or q <= n
    ):
        return ()
    source_group = TodaPrimaryGroup(q - 1, n - 1)
    injective = MapInjective(TodaSuspensionMap(source_group, goal.group))
    matched: list[Relation] = []
    for claim in available:
        if (
            not isinstance(claim, Relation)
            or claim.relation_type is not RelationType.EQUALITY
            or claim.lhs != source_group
            or not isinstance(claim.rhs, FiniteCyclicGroup)
            or nonzero_cyclic_generator_image(claim, injective, goal.element) != goal
        ):
            continue
        if claim not in matched:
            matched.append(claim)
    if len(matched) != 1:
        return ()
    source = matched[0]
    return (
        GoalExpansion(
            injected_generator_nonzero_rule(goal, source, injective),
            (source, injective),
        ),
    )

def expand_public_nonzero_double_from_cited_source(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer a double-nonzero proof from screened equations and typed prior goals.

    A structured database generator supplies only a *candidate* image goal.
    The earlier cyclic group relation and the cited double relation must be
    present in screened source claims; both inferred premises are reconstructed
    in the public recursive search. No database goal is accepted as a proof.
    """
    from phase165_r3_recursive_search import GoalExpansion
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase166_r3aj_structured_generator import (
        database_structured_group_goal_candidates,
    )
    from phase171_r2j_r4_r3_double_image_bridge.source import (
        typed_double_image_conclusion,
    )

    if not isinstance(available, tuple):
        raise TypeError("available must contain screened fixed statements")
    if (
        not isinstance(goal, NonZeroGroupElement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or not isinstance(goal.element, Multiple)
        or type(goal.element.coefficient) is not int
        or goal.element.coefficient != 2
    ):
        return ()
    group = goal.group
    q, n = group.group_dimension, group.sphere_dimension
    if (
        type(q) is not int
        or type(n) is not int
        or n < 3
        or q <= n
        or _endpoints(goal.element.expression) != (q, n)
    ):
        return ()
    earlier_group = TodaPrimaryGroup(q - 1, n - 1)
    injection = MapInjective(TodaSuspensionMap(earlier_group, group))
    prior_sources = tuple(
        claim for claim in available
        if isinstance(claim, Relation)
        and claim.relation_type is RelationType.EQUALITY
        and claim.lhs == earlier_group
        and isinstance(claim.rhs, FiniteCyclicGroup)
        and type(claim.rhs.order) is int
        and claim.rhs.order > 1
    )
    # The structured database is used to type a goal, NEVER to establish the
    # earlier group as a premise or produce a GIVEN.
    typed_candidates = database_structured_group_goal_candidates(
        n=n - 1, k=q - n,
    )
    double_sources = tuple(
        claim for claim in available
        if isinstance(claim, Relation)
        and claim.relation_type is RelationType.EQUALITY
        and claim.lhs == goal.element
    )
    proposals: list[GoalExpansion] = []
    for prior in prior_sources:
        for typed in typed_candidates:
            if (
                not isinstance(typed, Relation)
                or typed.relation_type is not RelationType.EQUALITY
                or typed.lhs != earlier_group
                or not isinstance(typed.rhs, FiniteCyclicGroup)
                or typed.rhs.order != prior.rhs.order
                or not same_registered_group_presentation(prior.rhs, typed.rhs)
            ):
                continue
            for cited_double in double_sources:
                image = GeneratorImage(
                    map=TodaSuspensionMap(earlier_group, group),
                    source_generator=typed.rhs.generator,
                    target_generator=cited_double.rhs,
                )
                typed_equality = typed_double_image_conclusion(
                    cited_double, image,
                )
                if typed_equality is None:
                    continue
                nonzero_image = NonZeroGroupElement(group, typed_equality.rhs)
                if (
                    nonzero_cyclic_generator_image(
                        prior, injection, typed_equality.rhs,
                    ) != nonzero_image
                    or nonzero_double_from_equality(
                        typed_equality, nonzero_image,
                    ) != goal
                ):
                    continue
                option = GoalExpansion(
                    inferred_nonzero_double_rule(
                        goal, typed_equality, nonzero_image,
                    ),
                    (typed_equality, nonzero_image),
                )
                if not any(
                    existing.subgoals == option.subgoals
                    and existing.rule.name == option.rule.name
                    for existing in proposals
                ):
                    proposals.append(option)
    # Alternative source-grounded proofs may coexist; recursive search takes
    # the first completed certified derivation, not a uniquely chosen route.
    # Direct-reference ambiguity is still checked by the search itself.
    return tuple(proposals)
