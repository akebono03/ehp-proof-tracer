"""Generic free-to-finite cyclic Delta kernel inference, requiring three proofs.

This module does not register a source, create a GIVEN, or attach a provider.
A proposed GoalExpansion is not a certified ProofStep.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import valid_ehp_lower_delta
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


RULE_NAME = "free-to-finite cyclic Delta generator kernel from three verified premises"


def expression_coordinates(value: object) -> tuple[int, int] | None:
    """Read actual domain/codomain of a typed element or composition, not a label."""
    if type(value) is HomotopyElement:
        if (type(value.source) is int and type(value.target) is int
                and value.source >= value.target >= 2):
            return value.source, value.target
        return None
    if type(value) in (Suspension, IteratedSuspension):
        source = value.source
        target = value.target
        if (type(source) is int and type(target) is int
                and source >= target >= 2):
            return source, target
        return None
    if type(value) is Composition:
        left = expression_coordinates(value.left)
        right = expression_coordinates(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return None


def conditional_inputs(
    goal: object,
    domain: object,
    codomain: object,
    signed_image: object,
) -> tuple[Relation, Relation, TodaDeltaImageUpToSignStatement] | None:
    """Require matching typed groups, generator and image; do not certify inputs."""
    if type(goal) is not KernelMultipleStatement:
        return None
    delta = goal.map
    if (type(delta) is not TodaDeltaMap
            or not valid_ehp_lower_delta(delta)
            or goal.domain != delta.source_group):
        return None
    if (type(domain) is not Relation
            or domain.relation_type is not RelationType.EQUALITY
            or domain.lhs != delta.source_group
            or type(domain.rhs) is not FreeCyclicGroup
            or domain.rhs.generator != goal.source_generator
            or expression_coordinates(domain.rhs.generator) != (
                delta.source_group.group_dimension,
                delta.source_group.sphere_dimension,
            )):
        return None
    if (type(codomain) is not Relation
            or codomain.relation_type is not RelationType.EQUALITY
            or codomain.lhs != delta.target_group
            or type(codomain.rhs) is not FiniteCyclicGroup
            or type(codomain.rhs.order) is not int
            or codomain.rhs.order < 1
            or codomain.rhs.order != goal.multiple
            or expression_coordinates(codomain.rhs.generator) != (
                delta.target_group.group_dimension,
                delta.target_group.sphere_dimension,
            )):
        return None
    if (type(signed_image) is not TodaDeltaImageUpToSignStatement
            or signed_image.map != delta
            or signed_image.element != domain.rhs.generator
            or signed_image.positive_value != codomain.rhs.generator):
        return None
    return domain, codomain, signed_image


def cyclic_delta_kernel_rule(
    goal: KernelMultipleStatement,
    domain: Relation,
    codomain: Relation,
    signed_image: TodaDeltaImageUpToSignStatement,
) -> InferenceRule:
    """Build a proof rule only for three structurally verified antecedents."""
    if conditional_inputs(goal, domain, codomain, signed_image) is None:
        raise ValueError("Three cyclic Delta kernel antecedents are incompatible")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.GIVEN
            and premises[2].rule is ProofRule.GIVEN
            and conditional_inputs(
                goal, premises[0].conclusion,
                premises[1].conclusion, premises[2].conclusion,
            ) == (domain, codomain, signed_image)
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "A map Z{g} to Z/m{h}, sending g to +/-h, has kernel <m*g>. "
            "Requires an independently inferred source presentation and "
            "two separately cited target/image facts."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, statement_pattern=domain),
            PremisePattern(statement_type=Relation, statement_pattern=codomain),
            PremisePattern(
                statement_type=TodaDeltaImageUpToSignStatement,
                statement_pattern=signed_image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cyclic_delta_kernel(
    goal: object,
    available_statements: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose a proof only when two distinct earlier typed source facts exist."""
    if not isinstance(available_statements, tuple):
        raise TypeError("available_statements must be a tuple")
    if type(goal) is not KernelMultipleStatement:
        return ()
    delta = goal.map
    if (type(delta) is not TodaDeltaMap
            or not valid_ehp_lower_delta(delta)
            or goal.domain != delta.source_group):
        return ()
    signed = tuple(
        item for item in available_statements
        if type(item) is TodaDeltaImageUpToSignStatement
        and item.map == delta
        and item.element == goal.source_generator
    )
    if len(signed) != 1:
        return ()
    target = tuple(
        item for item in available_statements
        if type(item) is Relation
        and item.relation_type is RelationType.EQUALITY
        and item.lhs == delta.target_group
        and type(item.rhs) is FiniteCyclicGroup
        and item.rhs.order == goal.multiple
        and item.rhs.generator == signed[0].positive_value
    )
    if len(target) != 1:
        return ()
    domain = Relation(
        delta.source_group,
        FreeCyclicGroup(goal.source_generator),
        RelationType.EQUALITY,
    )
    if conditional_inputs(goal, domain, target[0], signed[0]) is None:
        return ()
    return (
        GoalExpansion(
            rule=cyclic_delta_kernel_rule(goal, domain, target[0], signed[0]),
            subgoals=(domain, target[0], signed[0]),
        ),
    )
