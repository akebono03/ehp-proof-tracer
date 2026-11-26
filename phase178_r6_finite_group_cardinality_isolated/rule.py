"""Infer cardinality from a proved finite cyclic or direct sum presentation."""
from __future__ import annotations

from math import prod

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import (
    group_endpoints, valid_order,
)
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = 'finite cyclic presentation or finite direct sum implies group cardinality'


def cardinality_from_presentation(presentation: object) -> FiniteGroupCardinality | None:
    """Validate the structure and compute a candidate, not a proof."""
    if (type(presentation) is not Relation
            or presentation.relation_type is not RelationType.EQUALITY):
        return None
    endpoints = group_endpoints(presentation.lhs)
    if endpoints is None:
        return None
    structure = presentation.rhs
    if type(structure) is FiniteCyclicGroup:
        parts = (structure,)
    elif type(structure) is DirectSumGroup:
        parts = structure.summands
        if type(parts) is not tuple or len(parts) < 2:
            return None
    else:
        return None
    generators = []
    for part in parts:
        if (type(part) is not FiniteCyclicGroup
                or not valid_order(part.order)
                or typed_endpoints(part.generator) != endpoints
                or part.generator in generators):
            return None
        generators.append(part.generator)
    return FiniteGroupCardinality(presentation.lhs, prod(part.order for part in parts))


def cardinality_inputs(goal: object, presentation: object):
    if (type(goal) is not FiniteGroupCardinality
            or type(goal.order) is not int or goal.order < 2
            or group_endpoints(goal.group) is None
            or cardinality_from_presentation(presentation) != goal):
        return None
    return (presentation,)


def expand_finite_cardinality_from_presentation(goal: object, presentation: object):
    required = cardinality_inputs(goal, presentation)
    if required is None:
        return ()

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                and premises[0].conclusion == presentation
                and cardinality_inputs(goal, premises[0].conclusion) == required)

    rule = InferenceRule(
        name=RULE_NAME,
        description=(
            'A proved finite cyclic group has its listed order as cardinality. '
            'A proved finite direct sum of finite cyclic groups has cardinality '
            'equal to the product of the summand orders.'
        ),
        premise_patterns=(PremisePattern(statement_type=Relation,
                                         relation_type=RelationType.EQUALITY,
                                         statement_pattern=presentation),),
        match_guard=guard,
        conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, required),)
