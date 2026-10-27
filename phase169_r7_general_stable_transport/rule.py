"""Phase 169 R7: source-screened, arbitrary-fold stable cyclic transport.

No group answer or generator image is introduced as GIVEN.  Intermediate
expressions are typed *goals*, never a certificate that they are equal.
Existing eta-family rules may discharge the image goals; unknown families
remain unresolved rather than silently normalized from a DB label.
"""
from __future__ import annotations

from dataclasses import replace

from expression import (
    Composition,
    GeneratorSymbol,
    HomotopyElement,
    IteratedSuspension,
    Multiple,
    Sum,
)
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


_SUBSCRIPT = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _indexed_display(element: HomotopyElement) -> bool:
    """Check a conventional indexed spelling; the name is NOT proof evidence."""
    symbol = element.generator
    if not isinstance(symbol, GeneratorSymbol) or type(symbol.index) is not int:
        return False
    family = symbol.family
    index = symbol.index
    return element.name in (family + "_" + str(index),
                            family + str(index).translate(_SUBSCRIPT))


def _intermediate_typed_generator(source: object, target: object, step: int,
                                  exponent: int) -> object | None:
    """Construct a candidate intermediate term, not a proved identification.

    Every index/dimension change is checked structurally against *both*
    endpoints.  Missing name metadata fails closed.  Named intermediate
    expressions still require independent GeneratorImage proof steps.
    """
    if type(step) is not int or type(exponent) is not int or not 0 <= step <= exponent:
        return None
    if step == 0:
        return source
    if step == exponent:
        return target
    if isinstance(source, HomotopyElement) and isinstance(target, HomotopyElement):
        s, t = source.generator, target.generator
        if not (isinstance(s, GeneratorSymbol) and isinstance(t, GeneratorSymbol)
                and s.family == t.family and s.decoration == t.decoration
                and type(s.index) is int and type(t.index) is int
                and t.index - s.index == exponent
                and all(type(x) is int for x in (
                    source.dimension, target.dimension,
                    source.source, target.source, source.target, target.target))
                and target.dimension - source.dimension == exponent
                and target.source - source.source == exponent
                and target.target - source.target == exponent
                and _indexed_display(source) and _indexed_display(target)):
            return None
        middle_index = s.index + step
        return replace(
            source,
            name=s.family + str(middle_index).translate(_SUBSCRIPT),
            dimension=source.dimension + step,
            source=source.source + step,
            target=source.target + step,
            generator=replace(s, index=middle_index),
        )
    if isinstance(source, Composition) and isinstance(target, Composition):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Composition(left, right) if left is not None and right is not None else None
    if isinstance(source, Sum) and isinstance(target, Sum):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Sum(left, right) if left is not None and right is not None else None
    if (isinstance(source, Multiple) and isinstance(target, Multiple)
            and source.coefficient == target.coefficient):
        inner = _intermediate_typed_generator(source.expression, target.expression,
                                              step, exponent)
        return Multiple(source.coefficient, inner) if inner is not None else None
    if (isinstance(target, IteratedSuspension)
            and target.expression == source
            and type(target.exponent) is int
            and target.exponent == exponent):
        return IteratedSuspension(source, step)
    if (isinstance(source, IteratedSuspension)
            and isinstance(target, IteratedSuspension)
            and source.expression == target.expression
            and type(source.exponent) is int
            and type(target.exponent) is int
            and target.exponent - source.exponent == exponent):
        return IteratedSuspension(source.expression, source.exponent + step)
    return None


def _consecutive_generator_image_goals(source: Relation, target: Relation
                                       ) -> tuple[GeneratorImage, ...] | None:
    """Build r consecutive, independently provable element-image obligations."""
    if not (isinstance(source, Relation) and isinstance(target, Relation)
            and source.relation_type is RelationType.EQUALITY
            and target.relation_type is RelationType.EQUALITY
            and isinstance(source.lhs, TodaPrimaryGroup)
            and isinstance(target.lhs, TodaPrimaryGroup)
            and isinstance(source.rhs, FiniteCyclicGroup)
            and isinstance(target.rhs, FiniteCyclicGroup)
            and source.rhs.order == target.rhs.order):
        return None
    n, q = source.lhs.sphere_dimension, source.lhs.group_dimension
    m, p = target.lhs.sphere_dimension, target.lhs.group_dimension
    if (not all(type(v) is int for v in (n, q, m, p))
            or n < 2 or q < n or n < (q - n) + 2
            or m <= n or p - q != m - n):
        return None
    r = m - n
    generators = tuple(
        _intermediate_typed_generator(source.rhs.generator,
                                      target.rhs.generator, i, r)
        for i in range(r + 1)
    )
    if any(g is None for g in generators):
        return None
    return tuple(
        GeneratorImage(
            map=TodaSuspensionMap(
                TodaPrimaryGroup(q + i, n + i),
                TodaPrimaryGroup(q + i + 1, n + i + 1),
            ),
            source_generator=generators[i],
            target_generator=generators[i + 1],
        )
        for i in range(r)
    )


def general_stable_cyclic_transport_rule(goal: Relation, source: Relation) -> InferenceRule:
    """Prove arbitrary-fold transport with exactly bound, proved premises.

    Statement patterns bind each specific image to its own slot.  Matching
    therefore does not enumerate the factorial permutations of r images.
    """
    if not (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(goal.rhs, FiniteCyclicGroup)):
        raise TypeError("a typed finite-cyclic group goal is required")
    images = _consecutive_generator_image_goals(source, goal)
    if images is None:
        raise ValueError("source and target must satisfy the stable typed transport shape")
    concrete_iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=len(images), source_group=source.lhs, target_group=goal.lhs,
    ))
    expected = (source, concrete_iso) + images

    def guard(premises, bindings):
        return (len(premises) == len(expected)
                and all(step.rule is ProofRule.INFERENCE for step in premises[1:])
                and tuple(step.conclusion for step in premises) == expected
                and _consecutive_generator_image_goals(source, goal) == images)

    return InferenceRule(
        name="prior cited arbitrary-fold stable cyclic generator transport",
        description=(
            "Use a publication-eligible earlier group, an independently proved "
            "Toda (4.5) isomorphism and a chain of independently proved "
            "generator images. Never identify a DB label by stable range alone."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=source),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Toda45IsomorphismStatement,
                           statement_pattern=concrete_iso),
        ) + tuple(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=GeneratorImage, statement_pattern=image)
            for image in images
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_prior_general_stable_transport(
    goal: object,
    available: tuple[object, ...],
    bridge: RegistryBridgeResult,
    *,
    proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Offer the earliest eligible stable source as a genuine proof subgoal.

    Intermediate named generators are proposed as image goals.  The common
    recursive solver must prove every one of them separately.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be tuple")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if goal != proof_target or not (
            isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(goal.rhs, FiniteCyclicGroup)):
        return ()
    target_n, target_q = goal.lhs.sphere_dimension, goal.lhs.group_dimension
    if (type(target_n) is not int or type(target_q) is not int
            or target_q <= target_n or target_n < 3):
        return ()
    stem = target_q - target_n
    base_n = stem + 2
    if target_n <= base_n:
        return ()
    citing_id = resolve_specialized_goal_citing_id(bridge, proof_target)
    if citing_id is None:
        return ()
    for source_n in range(base_n, target_n):
        prior = resolve_prior_group_result(
            bridge, source_n=source_n, source_k=stem,
            citing_assertion_id=citing_id,
        )
        if not prior.eligible or prior.source_assertion_id is None or prior.relation is None:
            continue
        source = prior.relation
        images = _consecutive_generator_image_goals(source, goal)
        if images is None:
            continue
        concrete_iso = Toda45IsomorphismStatement(
            map=TodaIteratedSuspensionMap(
                exponent=len(images),
                source_group=source.lhs,
                target_group=goal.lhs,
            )
        )
        if not any(
            isinstance(schema, Toda45IsomorphismStatement)
            and (schema == concrete_iso
                 or specialize_typed_statement(schema, concrete_iso) is not None)
            for schema in available
        ):
            continue
        return (GoalExpansion(
            general_stable_cyclic_transport_rule(goal, source),
            (source, concrete_iso) + images,
        ),)
    return ()
