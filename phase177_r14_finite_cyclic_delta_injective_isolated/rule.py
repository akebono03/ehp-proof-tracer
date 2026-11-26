"""Conditional order and injectivity rules; no provider or registered proof leaves."""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import valid_ehp_lower_delta
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

ORDER_RULE = 'finite direct summand generator has its summand order'
INJECTIVE_RULE = 'finite cyclic source and full order generator image imply Delta injectivity'


def group_endpoints(group: object) -> tuple[int, int] | None:
    if type(group) is not TodaPrimaryGroup:
        return None
    q, n = group.group_dimension, group.sphere_dimension
    if type(q) is not int or type(n) is not int or n < 2 or q < n:
        return None
    return q, n


def valid_order(value: object) -> bool:
    return type(value) is int and value >= 2


def summand_order_inputs(goal: object, presentation: object):
    """Exact typed identity only; every summand must be explicitly cyclic."""
    if type(goal) is not FiniteElementOrder or not valid_order(goal.order):
        return None
    endpoints = group_endpoints(goal.group)
    if (endpoints is None or typed_endpoints(goal.element) != endpoints
            or type(presentation) is not Relation
            or presentation.relation_type is not RelationType.EQUALITY
            or presentation.lhs != goal.group
            or type(presentation.rhs) is not DirectSumGroup):
        return None
    parts = presentation.rhs.summands
    if type(parts) is not tuple or len(parts) < 2:
        return None
    seen = []
    matches = []
    for part in parts:
        if type(part) not in (FiniteCyclicGroup, FreeCyclicGroup):
            return None
        if type(part) is FiniteCyclicGroup and not valid_order(part.order):
            return None
        if typed_endpoints(part.generator) != endpoints or part.generator in seen:
            return None
        seen.append(part.generator)
        if part.generator == goal.element:
            matches.append(part)
    if len(matches) != 1 or type(matches[0]) is not FiniteCyclicGroup:
        return None
    if matches[0].order != goal.order:
        return None
    return (presentation,)


def finite_delta_injective_inputs(goal: object, domain: object, image: object, order: object):
    """The image must have exactly the proved finite cyclic domain order."""
    if type(goal) is not MapInjective or not valid_ehp_lower_delta(goal.map):
        return None
    delta = goal.map
    source, target = group_endpoints(delta.source_group), group_endpoints(delta.target_group)
    if source is None or target is None:
        return None
    if (type(domain) is not Relation or domain.relation_type is not RelationType.EQUALITY
            or domain.lhs != delta.source_group or type(domain.rhs) is not FiniteCyclicGroup
            or not valid_order(domain.rhs.order)
            or typed_endpoints(domain.rhs.generator) != source):
        return None
    if (type(image) is not GeneratorImage or image.map != delta
            or image.source_generator != domain.rhs.generator
            or typed_endpoints(image.target_generator) != target):
        return None
    if (type(order) is not FiniteElementOrder or order.group != delta.target_group
            or order.element != image.target_generator or not valid_order(order.order)
            or order.order != domain.rhs.order):
        return None
    return domain, image, order


def expand_summand_generator_order(goal: object, presentation: object):
    required = summand_order_inputs(goal, presentation)
    if required is None:
        return ()

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                and premises[0].conclusion == presentation
                and summand_order_inputs(goal, premises[0].conclusion) == required)

    rule = InferenceRule(
        name=ORDER_RULE,
        description='In a proved direct sum, the inclusion of a finite cyclic summand preserves the exact order of its listed generator.',
        premise_patterns=(PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                                         statement_pattern=presentation),),
        match_guard=guard,
        conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, required),)


def expand_finite_delta_injective(goal: object, domain: object, image: object, order: object):
    required = finite_delta_injective_inputs(goal, domain, image, order)
    if required is None:
        return ()

    def guard(premises, bindings):
        return (len(premises) == 3
                and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                and all(p.rule is ProofRule.INFERENCE for p in premises[1:])
                and tuple(p.conclusion for p in premises) == required
                and finite_delta_injective_inputs(goal, *(p.conclusion for p in premises)) == required)

    rule = InferenceRule(
        name=INJECTIVE_RULE,
        description='For a homomorphism from a finite cyclic group of order m, a generator image of exact order m forces the kernel to be zero.',
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY, statement_pattern=domain),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=GeneratorImage, statement_pattern=image),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=FiniteElementOrder, statement_pattern=order),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, required),)
