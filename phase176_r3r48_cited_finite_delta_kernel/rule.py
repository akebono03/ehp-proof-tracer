"""Finite-to-finite cyclic Delta kernel; no target-specific mathematics."""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import valid_ehp_lower_delta
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import expression_coordinates
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionOrigin

RULE_NAME = 'finite-to-finite cyclic Delta generator kernel from verified premises'


def conditional_inputs(goal, domain, codomain, signed_image):
    """Validate the typed mathematical hypotheses independently of provenance."""
    if type(goal) is not KernelMultipleStatement:
        return None
    delta = goal.map
    if (type(delta) is not TodaDeltaMap or not valid_ehp_lower_delta(delta)
            or goal.domain != delta.source_group):
        return None
    for relation, group in ((domain, delta.source_group), (codomain, delta.target_group)):
        if (type(relation) is not Relation or relation.relation_type is not RelationType.EQUALITY
                or relation.lhs != group or type(relation.rhs) is not FiniteCyclicGroup
                or type(relation.rhs.order) is not int or relation.rhs.order < 1
                or expression_coordinates(relation.rhs.generator) != (
                    group.group_dimension, group.sphere_dimension)):
            return None
    M, m = domain.rhs.order, codomain.rhs.order
    if (type(goal.multiple) is not int or goal.multiple != m or M % m
            or goal.source_generator != domain.rhs.generator):
        return None
    if (type(signed_image) is not TodaDeltaImageUpToSignStatement
            or signed_image.map != delta or signed_image.element != domain.rhs.generator
            or signed_image.positive_value != codomain.rhs.generator):
        return None
    return domain, codomain, signed_image


def linked_cited_steps(bridge, statement):
    """Find exact, positioned, linked fixed GIVENs in the active source context."""
    steps = []
    for link in bridge.proof_links:
        step = link.step
        if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                or step.premises or type(step.conclusion) is not type(statement)
                or step.conclusion != statement):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        ref = bridge.registry.reference(assertion.reference_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or type(assertion.content) is not type(statement) or assertion.content != statement
                or type(ref.publication_position) is not int or ref.publication_position <= 0
                or step.inference_rule is None or step.inference_rule.literature_reference is None):
            continue
        steps.append(step)
    return tuple(steps)


def finite_cyclic_delta_kernel_rule(goal, domain, codomain, signed_image, *, proof_target, bridge):
    """Actual proof steps, not the candidate presentations, discharge the premises."""
    required = conditional_inputs(goal, domain, codomain, signed_image)
    if required is None:
        raise ValueError('incompatible finite cyclic Delta kernel premises')

    def group_verified(step):
        # Cited source has priority in DFS; DB GIVENs are independently revalidated.
        if step.rule is ProofRule.INFERENCE:
            return bool(step.premises) and step.inference_rule is not None
        return (verified_db_step(step, proof_target=proof_target, bridge=bridge)
                or step in linked_cited_steps(bridge, step.conclusion))

    def guard(premises, bindings):
        return (len(premises) == 3
                and tuple(step.conclusion for step in premises) == required
                and conditional_inputs(goal, *(step.conclusion for step in premises)) == required
                and all(group_verified(step) for step in premises[:2])
                and len(linked_cited_steps(bridge, signed_image)) == 1
                and premises[2] in linked_cited_steps(bridge, signed_image))

    return InferenceRule(
        name=RULE_NAME,
        description=('For Z/M{a} to Z/m{b}, m divides M and Delta(a)=+/-b; '
                     'the kernel consists of multiples of m*a, whose order is M/m. '
                     'The two presentations and the signed image must be proved independently.'),
        premise_patterns=(PremisePattern(statement_type=Relation, statement_pattern=domain),
                          PremisePattern(statement_type=Relation, statement_pattern=codomain),
                          PremisePattern(statement_type=TodaDeltaImageUpToSignStatement,
                                         statement_pattern=signed_image, proof_rule=ProofRule.GIVEN)),
        conclusion_pattern=goal, match_guard=guard,
    )
