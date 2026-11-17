"""A proved finite-cyclic direct summand annihilates its typed generator.

Works for a single FiniteCyclicGroup and for each finite cyclic summand of a
DirectSumGroup, including nested sums. No group presentation is asserted here.
A source-first caller supplies concrete candidate presentations to the
backward provider; the ordinary engine must prove the chosen premise.
"""
from __future__ import annotations

from expression import (
    Composition, HomotopyElement, IteratedSuspension, Multiple,
    Sum, Suspension, Zero,
)
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup,
)
from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule, PremisePattern, ProofRule, Relation, RelationType,
)

RULE_NAME = "proved finite cyclic summand order annihilates its generator"


def typed_endpoints(element: object) -> tuple[int, int] | None:
    """Return (source dimension, sphere dimension) when endpoints are typed."""
    if isinstance(element, HomotopyElement):
        if not all(type(value) is int for value in (
            element.dimension, element.source, element.target,
        )):
            return None
        if (element.dimension != element.target or element.target < 2
                or element.source <= element.target):
            return None
        return element.source, element.target
    if isinstance(element, Composition):
        left = typed_endpoints(element.left)
        right = typed_endpoints(element.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    if isinstance(element, Suspension):
        pair = typed_endpoints(element.expression)
        if pair is None:
            return None
        return pair[0] + 1, pair[1] + 1
    if isinstance(element, IteratedSuspension):
        if type(element.exponent) is not int or element.exponent < 0:
            return None
        pair = typed_endpoints(element.expression)
        if pair is None:
            return None
        return pair[0] + element.exponent, pair[1] + element.exponent
    if isinstance(element, Multiple):
        if type(element.coefficient) is not int:
            return None
        return typed_endpoints(element.expression)
    if isinstance(element, Sum):
        left = typed_endpoints(element.left)
        right = typed_endpoints(element.right)
        if left is None or left != right:
            return None
        return left
    return None


def _finite_cyclic_components(structure: object) -> tuple[FiniteCyclicGroup, ...]:
    """Traverse only actual finite cyclic components of a typed presentation."""
    if isinstance(structure, FiniteCyclicGroup):
        if type(structure.order) is int and structure.order >= 2:
            return (structure,)
        return ()
    if not isinstance(structure, DirectSumGroup):
        return ()
    components: list[FiniteCyclicGroup] = []
    for summand in structure.summands:
        components.extend(_finite_cyclic_components(summand))
    return tuple(components)


def order_zero_premise(
    goal: object, presentation: Relation | None = None,
) -> Relation | None:
    """Validate one candidate source, never infer an arbitrary complement.

    No presentation: preserve the R4R5R1 single-cyclic backward obligation.
    Supplied presentation: require the exact target generator as a finite
    cyclic summand with the specified order, and matching sphere endpoints.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type not in (RelationType.EQUALITY, RelationType.ZERO)
            or type(goal.lhs) is not Multiple
            or type(goal.lhs.coefficient) is not int
            or goal.lhs.coefficient < 2
            or type(goal.rhs) is not Zero
            or goal.source is not None
            or goal.note is not None):
        return None
    endpoints = typed_endpoints(goal.lhs.expression)
    if endpoints is None:
        return None
    source, target = endpoints
    group = TodaPrimaryGroup(source, target)
    if presentation is None:
        return Relation(
            lhs=group,
            rhs=FiniteCyclicGroup(goal.lhs.coefficient, goal.lhs.expression),
            relation_type=RelationType.EQUALITY,
        )
    if (not isinstance(presentation, Relation)
            or presentation.relation_type is not RelationType.EQUALITY
            or presentation.lhs != group):
        return None
    for summand in _finite_cyclic_components(presentation.rhs):
        if (summand.order == goal.lhs.coefficient
                and summand.generator == goal.lhs.expression):
            return presentation
    return None


def finite_cyclic_order_zero_rule(
    goal: Relation, presentation: Relation | None = None,
) -> InferenceRule:
    """One-premise ordinary rule, binding the *entire* group presentation."""
    expected = order_zero_premise(goal, presentation)
    if expected is None:
        raise ValueError("goal must be a typed finite-order generator zero equality with a proved finite-cyclic summand presentation")

    def guard(premises, bindings) -> bool:
        return (
            len(premises) == 1
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[0].conclusion == expected
            and order_zero_premise(goal, expected) == expected
        )

    def conclusion_builder(premises) -> Relation:
        if (len(premises) != 1
                or premises[0].conclusion != expected
                or order_zero_premise(goal, expected) != expected):
            raise ValueError("the proved finite-cyclic summand is required")
        return goal

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "In a proved group presentation, every finite-cyclic summand "
            "Z/m{g} satisfies m*g=0. The presentation must be proved first."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=expected,
            ),
        ),
        conclusion_builder=conclusion_builder,
        match_guard=guard,
    )


def expand_finite_cyclic_order_zero(
    goal: object, presentations: tuple[Relation, ...] = (),
) -> tuple[GoalExpansion, ...]:
    """Provide source-first backward proposals for any verified component.

    With no source candidates retain the previous single-cyclic proposal.
    With source candidates, use only matching concrete presentations; do not
    fabricate complement groups or treat candidates as verified evidence.
    """
    if not isinstance(presentations, tuple):
        raise TypeError("presentations must be a tuple")
    if not presentations:
        premise = order_zero_premise(goal)
        if premise is None:
            return ()
        return (GoalExpansion(finite_cyclic_order_zero_rule(goal), (premise,)),)
    results: list[GoalExpansion] = []
    seen: list[Relation] = []
    for candidate in presentations:
        premise = order_zero_premise(goal, candidate)
        if premise is None or premise in seen:
            continue
        seen.append(premise)
        results.append(GoalExpansion(
            finite_cyclic_order_zero_rule(goal, premise), (premise,),
        ))
    return tuple(results)
