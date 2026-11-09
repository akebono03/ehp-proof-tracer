"""R32 read-only contract for a conditional free-to-finite cyclic Delta kernel.

This is NOT a production InferenceRule or a provider. Nothing here certifies
its three independent mathematical premises or creates a ProofStep.
"""
from __future__ import annotations

from expression import HomotopyElement
from homotopy_groups import (
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
)
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from proof import Relation, RelationType
from toda_rules import (
    TodaDeltaImageUpToSignStatement,
    TodaProp42ExactnessStatement,
)


def valid_ehp_lower_delta(delta: object) -> bool:
    """Reject map-shaped objects with invalid EHP H-Delta dimensions."""
    if type(delta) is not TodaDeltaMap:
        return False
    a, b = delta.source_group, delta.target_group
    if type(a) is not TodaPrimaryGroup or type(b) is not TodaPrimaryGroup:
        return False
    q, n = b.group_dimension, b.sphere_dimension
    if (type(q) is not int or type(n) is not int or n < 2 or q < n
            or a != TodaPrimaryGroup(q + 2, 2 * n + 1)):
        return False
    window = TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(q + 2, n + 1),
        middle_term=a,
        target_term=b,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
    )
    return prop42_exactness_indices(TodaProp42ExactnessStatement(window)) == (
        n, q + 2, "h_delta",
    )


def generator_has_group_coordinates(element: object, group: TodaPrimaryGroup) -> bool:
    """Accept only typed homotopy elements of precisely the requested group."""
    return (
        type(element) is HomotopyElement
        and type(element.source) is int
        and type(element.target) is int
        and element.source == group.group_dimension
        and element.target == group.sphere_dimension
    )


def conditional_kernel_premises(
    goal: object,
    domain_presentation: object,
    codomain_presentation: object,
    signed_generator_image: object,
) -> tuple[Relation, Relation, TodaDeltaImageUpToSignStatement] | None:
    """Check the hypotheses of ker(Delta)=<m*g>; never prove them.

    A group homomorphism Z{g} -> Z/m{h} with Delta(g)=+/-h has kernel
    <m*g>. Signed generator equality is exact: no symbolic normalization,
    group identification, unverified database reuse, or dimension guessing.
    """
    if type(goal) is not KernelMultipleStatement:
        return None
    delta = goal.map
    if not valid_ehp_lower_delta(delta) or goal.domain != delta.source_group:
        return None
    if (type(domain_presentation) is not Relation
            or domain_presentation.relation_type is not RelationType.EQUALITY
            or domain_presentation.lhs != delta.source_group
            or type(domain_presentation.rhs) is not FreeCyclicGroup):
        return None
    generator = domain_presentation.rhs.generator
    if (not generator_has_group_coordinates(generator, delta.source_group)
            or generator != goal.source_generator):
        return None
    if (type(codomain_presentation) is not Relation
            or codomain_presentation.relation_type is not RelationType.EQUALITY
            or codomain_presentation.lhs != delta.target_group
            or type(codomain_presentation.rhs) is not FiniteCyclicGroup):
        return None
    target_group = codomain_presentation.rhs
    if (type(target_group.order) is not int or target_group.order < 1
            or goal.multiple != target_group.order
            or not generator_has_group_coordinates(
                target_group.generator, delta.target_group,
            )):
        return None
    if (type(signed_generator_image) is not TodaDeltaImageUpToSignStatement
            or signed_generator_image.map != delta
            or signed_generator_image.element != generator
            or signed_generator_image.positive_value != target_group.generator):
        return None
    return domain_presentation, codomain_presentation, signed_generator_image


def signed_cyclic_kernel_membership(
    order: int, coefficient: int, sign: int,
) -> bool:
    """Arithmetic check supporting the conditional lemma, not a proof step."""
    if (type(order) is not int or order < 1
            or type(coefficient) is not int or type(sign) is not int
            or sign not in (-1, 1)):
        raise ValueError("requires a positive order, integer coefficient, and sign +/-1")
    return (sign * coefficient) % order == 0
