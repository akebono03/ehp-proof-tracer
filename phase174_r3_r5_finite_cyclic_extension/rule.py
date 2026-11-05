"""Phase 174 R3-R5: typed backward obligations for a cyclic index-two extension.

This module supplies two generic mathematical inferences, NOT new axioms.
Toda (4.8) remains a separate cited subgoal. The ordinary proof engine must
establish it and the Delta-zero, prior cyclic relation, and doubled relation.
No sphere dimension, generator name or bibliography ID is hard-coded.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaDeltaMap,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e5_composite_generator_image.rule import _endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaZeroStatement


@dataclass(frozen=True)
class Toda48UniversalConditionalStatement:
    """Citable source *obligation* for Toda (4.8), not an assumed citation.

    This phase does NOT register a GIVEN for this statement. Any future
    source bridge must independently verify text and publication precedence.
    """


@dataclass(frozen=True)
class Toda48IndexTwoDoubleSuspensionStatement:
    """E^2:A -> B is injective and B/E^2(A) has order two."""

    map: TodaIteratedSuspensionMap
    quotient_order: int = 2


def toda48_delta_goal(index_goal: object) -> TodaDeltaZeroStatement | None:
    """Check the entire even-n (4.8) geometry before proposing its Delta goal."""
    if not isinstance(index_goal, Toda48IndexTwoDoubleSuspensionStatement):
        return None
    mapping = index_goal.map
    if not isinstance(mapping, TodaIteratedSuspensionMap):
        return None
    if type(mapping.exponent) is not int or mapping.exponent != 2:
        return None
    if type(index_goal.quotient_order) is not int or index_goal.quotient_order != 2:
        return None
    a, b = mapping.source_group, mapping.target_group
    if not isinstance(a, TodaPrimaryGroup) or not isinstance(b, TodaPrimaryGroup):
        return None
    if any(type(x) is not int for x in (
        a.group_dimension, a.sphere_dimension,
        b.group_dimension, b.sphere_dimension,
    )):
        return None
    n = a.sphere_dimension + 1
    if n < 4 or n % 2 != 0:
        return None
    if a != TodaPrimaryGroup(2 * n - 2, n - 1):
        return None
    if b != TodaPrimaryGroup(2 * n, n + 1):
        return None
    return TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(2 * n - 1, 2 * n - 1),
        TodaPrimaryGroup(2 * n - 3, n - 1),
    ))


def toda48_index_two_inference_rule(
    goal: Toda48IndexTwoDoubleSuspensionStatement,
) -> InferenceRule:
    """Derive the conditional quotient and injection from cited (4.8) + Delta=0."""
    delta = toda48_delta_goal(goal)
    if delta is None:
        raise ValueError("invalid even-dimensional Toda (4.8) application")
    source = Toda48UniversalConditionalStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.GIVEN
            and premises[0].conclusion == delta
            and type(premises[1].conclusion) is Toda48UniversalConditionalStatement
            and premises[1].conclusion == source
            and toda48_delta_goal(goal) == delta
        )

    return InferenceRule(
        name="Toda (4.8) conditional index-two double suspension",
        description=(
            "The even-dimensional zero-Delta branch of Toda (4.8) makes E^2 "
            "injective and its image of index two. The stated condition and "
            "the source theorem must both be verified."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaDeltaZeroStatement,
                statement_pattern=delta,
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Toda48UniversalConditionalStatement,
                statement_pattern=source,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_toda48_index_two(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Put the verifiable Delta-zero subgoal before the cited-source obligation."""
    delta = toda48_delta_goal(goal)
    if delta is None:
        return ()
    return (GoalExpansion(
        toda48_index_two_inference_rule(goal),
        (delta, Toda48UniversalConditionalStatement()),
    ),)


def finite_index_two_cyclic_conclusion(
    index: object,
    prior: object,
    double: object,
) -> CyclicStructureStatement | None:
    """Group theorem: |A|=m even, [B:f(A)]=2, 2b=f(a) => B=<b>, |B|=2m.

    Because f is injective, 2b has order m. For even m the only possible
    order of b is 2m; the index-two formula gives |B|=2m, so b generates B.
    Both injectivity and the index-two quotient belong to the typed index
    statement; a merely presented map is insufficient proof evidence.
    """
    if (
        not isinstance(index, Toda48IndexTwoDoubleSuspensionStatement)
        or toda48_delta_goal(index) is None
        or not isinstance(prior, Relation)
        or prior.relation_type is not RelationType.EQUALITY
        or not isinstance(prior.lhs, TodaPrimaryGroup)
        or not isinstance(prior.rhs, FiniteCyclicGroup)
        or type(prior.rhs.order) is not int
        or prior.rhs.order < 2
        or prior.rhs.order % 2 != 0
        or not isinstance(double, Relation)
        or double.relation_type is not RelationType.EQUALITY
        or not isinstance(double.lhs, Multiple)
        or type(double.lhs.coefficient) is not int
        or double.lhs.coefficient != 2
        or not isinstance(double.rhs, IteratedSuspension)
        or type(double.rhs.exponent) is not int
        or double.rhs.exponent != 2
        or not isinstance(double.lhs.expression, HomotopyElement)
    ):
        return None
    mapping = index.map
    a, b = mapping.source_group, mapping.target_group
    source_generator = prior.rhs.generator
    target_generator = double.lhs.expression
    if (
        prior.lhs != a
        or not isinstance(source_generator, HomotopyElement)
        or double.rhs.expression != source_generator
        or _endpoints(source_generator) != (a.group_dimension, a.sphere_dimension)
        or _endpoints(target_generator) != (b.group_dimension, b.sphere_dimension)
        or (double.rhs.source, double.rhs.target) != (
            b.group_dimension, b.sphere_dimension,
        )
    ):
        return None
    return CyclicStructureStatement(b, target_generator, 2 * prior.rhs.order)


def finite_index_two_cyclic_rule(
    goal: CyclicStructureStatement,
    index: Toda48IndexTwoDoubleSuspensionStatement,
    prior: Relation,
    double: Relation,
) -> InferenceRule:
    """All substantive premises must be recovered through the proof search."""
    if finite_index_two_cyclic_conclusion(index, prior, double) != goal:
        raise ValueError("invalid typed finite cyclic extension premise configuration")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[2].rule is ProofRule.INFERENCE
            and premises[0].conclusion == index
            and premises[1].conclusion == prior
            and premises[2].conclusion == double
            and finite_index_two_cyclic_conclusion(
                premises[0].conclusion,
                premises[1].conclusion,
                premises[2].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="finite cyclic extension by an index-two injective image",
        description=(
            "An even-order cyclic subgroup embedded with index two is the "
            "double of an element precisely when the typed double relation "
            "identifies its generator; that element generates the extension."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Toda48IndexTwoDoubleSuspensionStatement,
                statement_pattern=index,
            ),
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=prior,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=double,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_finite_index_two_cyclic_structure(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Use earlier database presentations as candidate GOALS, never as proofs.

    The checked dimensions are derived from Toda (4.8), not from a named
    group, hard-coded dimension, or generator. No directly GIVEN group or
    doubled relation is manufactured.
    """
    if (
        not isinstance(goal, CyclicStructureStatement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or not isinstance(goal.generator, HomotopyElement)
        or type(goal.order) is not int
        or goal.order < 4
        or goal.order % 4 != 0
    ):
        return ()
    b = goal.group
    if (
        type(b.group_dimension) is not int
        or type(b.sphere_dimension) is not int
        or b.sphere_dimension < 5
        or _endpoints(goal.generator) != (
            b.group_dimension, b.sphere_dimension,
        )
    ):
        return ()
    n = b.sphere_dimension - 1
    a = TodaPrimaryGroup(b.group_dimension - 2, b.sphere_dimension - 2)
    mapping = TodaIteratedSuspensionMap(2, a, b)
    index = Toda48IndexTwoDoubleSuspensionStatement(mapping)
    if toda48_delta_goal(index) is None:
        return ()
    from phase166_r3aj_structured_generator import (
        database_structured_group_goal_candidates,
    )
    candidates = database_structured_group_goal_candidates(
        n=a.sphere_dimension, k=a.group_dimension - a.sphere_dimension,
    )
    options: list[GoalExpansion] = []
    for prior in candidates:
        if (
            not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != a
            or not isinstance(prior.rhs, FiniteCyclicGroup)
            or prior.rhs.order * 2 != goal.order
        ):
            continue
        double = Relation(
            Multiple(2, goal.generator),
            IteratedSuspension(prior.rhs.generator, 2),
            RelationType.EQUALITY,
        )
        if finite_index_two_cyclic_conclusion(index, prior, double) != goal:
            continue
        options.append(GoalExpansion(
            finite_index_two_cyclic_rule(goal, index, prior, double),
            (index, prior, double),
        ))
    # Avoid silently selecting between conflicting lower presentations.
    return tuple(options) if len(options) == 1 else ()
