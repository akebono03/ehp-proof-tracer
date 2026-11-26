"""Expose R14 rules as ordinary backward goals; never return proof steps."""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import valid_ehp_lower_delta
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import (
    expand_finite_delta_injective, expand_summand_generator_order, group_endpoints, valid_order,
)
from proof import Relation, RelationType


def presentation_candidates(group, *, bridge, proof_target):
    """Only source-linked presentations or existing ordered DB candidates."""
    if group_endpoints(group) is None:
        return ()
    result = []
    for link in bridge.proof_links:
        step = link.step
        item = None if step is None else step.conclusion
        if (type(item) is Relation and item.lhs == group
                and item.relation_type is RelationType.EQUALITY
                and type(item.rhs) in (FiniteCyclicGroup, DirectSumGroup)
                and item not in result and step in linked_cited_steps(bridge, item)):
            result.append(item)
    prior = admitted_prior_group_step(group, proof_target=proof_target, bridge=bridge)
    if (prior is not None and verified_db_step(prior, proof_target=proof_target, bridge=bridge)
            and type(prior.conclusion) is Relation
            and type(prior.conclusion.rhs) in (FiniteCyclicGroup, DirectSumGroup)
            and prior.conclusion not in result):
        result.append(prior.conclusion)
    return tuple(result)


def expand_from_presentations(goal, presentations):
    """Use the unchanged R14 rules, with every premise still an open goal."""
    options = []
    if type(goal) is FiniteElementOrder:
        for claim in presentations(goal.group):
            options.extend(expand_summand_generator_order(goal, claim))
    elif type(goal) is MapInjective and valid_ehp_lower_delta(goal.map):
        delta = goal.map
        for domain in presentations(delta.source_group):
            if type(domain) is not Relation or type(domain.rhs) is not FiniteCyclicGroup:
                continue
            m = domain.rhs.order
            if not valid_order(m):
                continue
            for codomain in presentations(delta.target_group):
                if (type(codomain) is not Relation or type(codomain.rhs) is not DirectSumGroup
                        or type(codomain.rhs.summands) is not tuple):
                    continue
                for part in codomain.rhs.summands:
                    if type(part) is not FiniteCyclicGroup or part.order != m:
                        continue
                    order = FiniteElementOrder(delta.target_group, part.generator, m)
                    if not expand_summand_generator_order(order, codomain):
                        continue
                    image = GeneratorImage(delta, domain.rhs.generator, part.generator)
                    for option in expand_finite_delta_injective(goal, domain, image, order):
                        if not any(old.rule.name == option.rule.name and old.subgoals == option.subgoals
                                   for old in options):
                            options.append(option)
    return tuple(options)


def build_public_finite_delta_injective_provider(*, bridge, proof_target):
    """No special dimensions or generators; DFS retains source and DB gates."""
    def presentations(group):
        return presentation_candidates(group, bridge=bridge, proof_target=proof_target)

    def expand(goal):
        return expand_from_presentations(goal, presentations)

    return expand
