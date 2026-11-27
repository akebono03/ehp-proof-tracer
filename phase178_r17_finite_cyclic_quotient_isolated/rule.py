"""Conditional finite cyclic EHP quotient, with no public wiring or new GIVEN."""
from math import gcd

from expression import Multiple
from homotopy_groups import (
    FiniteCyclicGroup, TodaDeltaMap, TodaEHPExactnessWindow,
    TodaPrimaryGroup, TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp42ExactnessStatement

RULE_NAME = 'EHP exact finite cyclic quotient by a signed generator multiple'


def finite_cyclic_quotient_inputs(goal, middle, source, signed, suspension):
    """Return six obligations for C --Delta--> A --E--> B, no assumed target.

    A=Z/N<a>, C=Z/M<z>, Delta(z)=+/-t*a, E(a)=b. Exactness and
    surjectivity imply B=Z/gcd(N,t)<b>. Require compatibility of orders.
    This rule covers nontrivial finite quotients only.
    """
    if type(goal) is not CyclicStructureStatement or type(goal.group) is not TodaPrimaryGroup:
        return None
    if type(goal.order) is not int or goal.order < 2:
        return None
    for presentation in (middle, source):
        if (type(presentation) is not Relation
                or presentation.relation_type is not RelationType.EQUALITY
                or type(presentation.lhs) is not TodaPrimaryGroup
                or type(presentation.rhs) is not FiniteCyclicGroup
                or type(presentation.rhs.order) is not int or presentation.rhs.order < 2):
            return None
        if typed_endpoints(presentation.rhs.generator) != (
                presentation.lhs.group_dimension, presentation.lhs.sphere_dimension):
            return None
    a, c, b = middle.lhs, source.lhs, goal.group
    for group in (a, c, b):
        if (type(group.group_dimension) is not int or type(group.sphere_dimension) is not int
                or group.sphere_dimension < 2 or group.group_dimension < group.sphere_dimension):
            return None
    if typed_endpoints(goal.generator) != (b.group_dimension, b.sphere_dimension):
        return None
    delta, e = TodaDeltaMap(c, a), TodaSuspensionMap(a, b)
    x, z = middle.rhs.generator, source.rhs.generator
    if (type(signed) is not TodaDeltaImageUpToSignStatement or signed.map != delta
            or signed.element != z or type(signed.positive_value) is not Multiple
            or signed.positive_value.expression != x):
        return None
    t = signed.positive_value.coefficient
    if type(t) is not int or t == 0:
        return None
    N, M = middle.rhs.order, source.rhs.order
    if (M * t) % N != 0 or gcd(N, t) != goal.order:
        return None
    if (type(suspension) is not GeneratorImage or suspension.map != e
            or suspension.source_generator != x or suspension.target_generator != goal.generator):
        return None
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=c, middle_term=a, target_term=b,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    ))
    if prop42_exactness_indices(exact) != (a.sphere_dimension, b.group_dimension, 'delta_e'):
        return None
    return middle, source, signed, exact, MapSurjective(e), suspension


def finite_cyclic_quotient_rule(goal, middle, source, signed, suspension, *, bridge):
    required = finite_cyclic_quotient_inputs(goal, middle, source, signed, suspension)
    if required is None or len(linked_cited_steps(bridge, signed)) != 1:
        raise ValueError('independent typed premises and one screened signed source required')

    def guard(premises, bindings):
        return (len(premises) == 6
                and tuple(p.conclusion for p in premises) == required
                and all(p.rule in (ProofRule.GIVEN, ProofRule.INFERENCE) for p in premises[:2])
                and len(linked_cited_steps(bridge, signed)) == 1
                and premises[2] in linked_cited_steps(bridge, signed)
                and all(p.rule is ProofRule.INFERENCE for p in premises[3:])
                and finite_cyclic_quotient_inputs(goal, middle, source, signed, suspension) == required)

    return InferenceRule(
        name=RULE_NAME,
        description=('For a finite cyclic middle group of order N, the signed image '
                     'of a source generator is t times its generator. Exactness gives '
                     'ker(E)=im(Delta)=<t*a>; if E is onto then the quotient has order '
                     'gcd(N,t), and the image of a generates it.'),
        premise_patterns=tuple(PremisePattern(
            statement_type=type(value), statement_pattern=value,
            relation_type=RelationType.EQUALITY if isinstance(value, Relation) else None,
            proof_rule=(ProofRule.GIVEN if i == 2 else ProofRule.INFERENCE if i >= 3 else None),
        ) for i, value in enumerate(required)),
        match_guard=guard, conclusion_pattern=goal,
    )


def expand_finite_cyclic_quotient(goal, middle, source, signed, suspension, *, bridge):
    required = finite_cyclic_quotient_inputs(goal, middle, source, signed, suspension)
    if required is None or len(linked_cited_steps(bridge, signed)) != 1:
        return ()
    return (GoalExpansion(finite_cyclic_quotient_rule(
        goal, middle, source, signed, suspension, bridge=bridge), required),)
