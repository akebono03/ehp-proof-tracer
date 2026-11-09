"""Source-bound public proposals for a cyclic suspension with zero image.

Reuses R6/R7/R9 and the existing compositional-image provider. A database
presentation selects an unproved GOAL only; it is never installed as a GIVEN.
A cited general annihilator is required to offer the composite-zero branch.
No target group, root result, or proof is registered by this module.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10b_registered_stable_family_binding.family_registry import (
    registered_family_of,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase169_r10eq_r1_universal_stable_definition.definition import (
    is_defined_stable_suspension,
    typed_element_span,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase174_r3_r7_r7_composite_zero_audit.rule import (
    expand_generator_zero_from_composite,
)
from phase174_r3_r7_r9_composition_associativity.rule import (
    expand_generator_image_associativity,
    typed_composition_factors,
)
from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
    canonical_annihilator_instance,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator,
)
from proof import Relation, RelationType


PROVIDER_ID = "phase174.r3.r7.r38.source_bound_zero_image_chain"


def valid_suspension(mapping: object) -> bool:
    """Require E:pi_q^n -> pi_(q+1)^(n+1) with concrete dimensions."""
    if type(mapping) is not TodaSuspensionMap:
        return False
    source, target = mapping.source_group, mapping.target_group
    if type(source) is not TodaPrimaryGroup or type(target) is not TodaPrimaryGroup:
        return False
    q, n = source.group_dimension, source.sphere_dimension
    return (type(q) is int and type(n) is int and n >= 2
            and q >= n and target == TodaPrimaryGroup(q + 1, n + 1))


def lifted_stable_composition(value: object) -> Composition | None:
    """Construct only definitional one-step suspensions of registered factors.

    The result is a GOAL for the existing proof engine, never a claimed image.
    """
    if type(value) is not Composition:
        return None

    def lift(part: object) -> object | None:
        if type(part) is HomotopyElement:
            family = registered_family_of(part)
            if family is None:
                return None
            n = part.dimension + 1
            if n < family.minimum_n:
                return None
            later = HomotopyElement(
                name=family.name_at(n), dimension=n,
                source=n + family.stem, target=n,
                generator=GeneratorSymbol(family.symbol_family, n),
            )
            return later if is_defined_stable_suspension(part, later) else None
        if type(part) is Composition:
            left, right = lift(part.left), lift(part.right)
            if left is None or right is None:
                return None
            result = Composition(left, right)
            return result if typed_element_span(result) is not None else None
        return None

    result = lift(value)
    return result if type(result) is Composition else None


def left_associated(value: Composition) -> Composition | None:
    """Preserve factors and their order; move parentheses only."""
    parts = typed_composition_factors(value)
    if parts is None or len(parts) < 3:
        return None
    result: object = parts[0]
    for part in parts[1:]:
        result = Composition(result, part)
    return result if type(result) is Composition and typed_element_span(result) == typed_element_span(value) else None


def expand_source_bound_zero_image_chain(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Only existing R6/R7/R9 INFERENCE options, with no new proof leaves."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    cited = tuple(item for item in available if type(item) is CitedFamilyAnnihilator)
    if len(cited) != 1:
        return ()

    if type(goal) is ImageZeroStatement:
        mapping = goal.map
        if not valid_suspension(mapping):
            return ()
        domain = mapping.source_group
        n, k = domain.sphere_dimension, domain.group_dimension - domain.sphere_dimension
        candidate = exact_prior_database_result(n, k)
        if (type(candidate) is not Relation
                or candidate.relation_type is not RelationType.EQUALITY
                or candidate.lhs != domain
                or type(candidate.rhs) is not FiniteCyclicGroup
                or candidate.rhs.order < 2
                or lifted_stable_composition(candidate.rhs.generator) is None):
            return ()
        # The DB object is only a subgoal; the proof engine must separately
        # discharge it under its established source-order and trust policy.
        return expand_zero_image_from_cyclic_generator(goal, candidate)

    if type(goal) is not GeneratorImage or not valid_suspension(goal.map):
        return ()
    source = goal.source_generator
    span = typed_element_span(source)
    mapping = goal.map
    if span != (
        mapping.source_group.group_dimension,
        mapping.source_group.sphere_dimension,
    ):
        return ()

    if type(goal.target_generator) is Zero:
        right = lifted_stable_composition(source)
        if right is None or typed_element_span(right) != (
            mapping.target_group.group_dimension,
            mapping.target_group.sphere_dimension,
        ):
            return ()
        left = left_associated(right)
        if left is None or type(left.left) is not Composition:
            return ()
        desired = Relation(left.left, Zero(), RelationType.EQUALITY)
        # Match the actual published general source schema. Merely constructing
        # this relation does not certify it or change its publication position.
        applicable = tuple(
            law for law in cited
            if type(left.left.left) is HomotopyElement
            and canonical_annihilator_instance(law, left.left.left.dimension) == desired
        )
        if len(applicable) != 1:
            return ()
        composite_image = GeneratorImage(mapping, source, left)
        return expand_generator_zero_from_composite(goal, composite_image)

    if type(goal.target_generator) is Composition:
        # The existing Phase 169 provider handles decomposing the correctly
        # associated composite into stable factor-image obligations.
        return expand_generator_image_associativity(goal)
    return ()
