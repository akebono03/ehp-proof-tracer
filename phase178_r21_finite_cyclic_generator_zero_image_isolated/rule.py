"""Isolated typed Delta specialization of the finite cyclic zero-image lemma."""
from expression import Zero
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_prior_group_step, group_coordinates, verified_db_step,
)
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import valid_ehp_lower_delta
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import finite_cyclic_presentation
from proof import InferenceRule, PremisePattern, ProofRule, Relation
from toda_rules import TodaDeltaZeroStatement

RULE_NAME = 'finite cyclic Delta generator zero implies typed Delta zero'


def valid_delta_zero_goal(goal):
    if type(goal) is not TodaDeltaZeroStatement or not valid_ehp_lower_delta(goal.map):
        return False
    a = goal.map.source_group
    return (type(a.group_dimension) is int and type(a.sphere_dimension) is int
            and a.group_dimension >= a.sphere_dimension)


def finite_cyclic_delta_zero_inputs(goal, presentation):
    """Return two typed obligations, not proofs or source claims."""
    if (not valid_delta_zero_goal(goal) or not finite_cyclic_presentation(presentation)
            or presentation.lhs != goal.map.source_group):
        return None
    return presentation, GeneratorImage(goal.map, presentation.rhs.generator, Zero())


def finite_cyclic_delta_zero_rule(goal, presentation, *, proof_target, bridge):
    """Accept only an admitted domain GIVEN and an exact linked zero-image GIVEN."""
    required = finite_cyclic_delta_zero_inputs(goal, presentation)
    if (required is None or not isinstance(bridge, RegistryBridgeResult)
            or group_coordinates(proof_target) is None
            or group_coordinates(presentation) == group_coordinates(proof_target)):
        raise ValueError('invalid finite cyclic Delta zero premises or proof context')

    def guard(premises, bindings):
        return (len(premises) == 2
                and all(step.rule is ProofRule.GIVEN for step in premises)
                and tuple(step.conclusion for step in premises) == required
                and finite_cyclic_delta_zero_inputs(goal, presentation) == required
                and (premises[0] in linked_cited_steps(bridge, required[0])
                     or verified_db_step(premises[0], proof_target=proof_target, bridge=bridge))
                and premises[1] in linked_cited_steps(bridge, required[1]))

    return InferenceRule(
        name=RULE_NAME,
        description=('A homomorphism from a finite cyclic group vanishes if its generator '
                     'maps to zero. Retain the admitted group and cited generator-image '
                     'GIVENs as separate premises; conclude the same typed Delta is zero.'),
        premise_patterns=(
            PremisePattern(statement_type=Relation, statement_pattern=required[0],
                           proof_rule=ProofRule.GIVEN),
            PremisePattern(statement_type=GeneratorImage, statement_pattern=required[1],
                           proof_rule=ProofRule.GIVEN),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def build_finite_cyclic_delta_zero_provider(*, bridge, proof_target):
    """Source-first proposals in a screened context; no public wiring in R21."""
    if not isinstance(bridge, RegistryBridgeResult) or group_coordinates(proof_target) is None:
        raise TypeError('screened registry bridge and group proof target required')

    def expand(goal):
        if not valid_delta_zero_goal(goal):
            return ()
        domain = goal.map.source_group
        presentations = []
        for link in bridge.proof_links:
            step = link.step
            claim = None if step is None else step.conclusion
            if (finite_cyclic_presentation(claim) and claim.lhs == domain
                    and group_coordinates(claim) != group_coordinates(proof_target)
                    and step in linked_cited_steps(bridge, claim)
                    and claim not in presentations):
                presentations.append(claim)
        prior = admitted_prior_group_step(domain, proof_target=proof_target, bridge=bridge)
        if (prior is not None and verified_db_step(prior, proof_target=proof_target, bridge=bridge)
                and prior.conclusion not in presentations):
            presentations.append(prior.conclusion)
        options = []
        for presentation in presentations:
            required = finite_cyclic_delta_zero_inputs(goal, presentation)
            if required is None or not linked_cited_steps(bridge, required[1]):
                continue
            options.append(GoalExpansion(finite_cyclic_delta_zero_rule(
                goal, presentation, proof_target=proof_target, bridge=bridge), required))
        return tuple(options)

    return expand
