"""Source-first proposals for the unchanged R17 finite cyclic quotient rule."""
from expression import Multiple
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from phase178_r17_finite_cyclic_quotient_isolated.rule import expand_finite_cyclic_quotient
from proof import Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


def build_public_finite_cyclic_quotient_provider(*, bridge, proof_target):
    """Discover screened source claims and earlier group goals, not proofs."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError('typed registry bridge required')

    def presentations(group):
        items = []
        for link in bridge.proof_links:
            step = link.step
            claim = None if step is None else step.conclusion
            if (type(claim) is Relation and claim.lhs == group
                    and claim.relation_type is RelationType.EQUALITY
                    and type(claim.rhs) is FiniteCyclicGroup
                    and step in linked_cited_steps(bridge, claim) and claim not in items):
                items.append(claim)
        prior = admitted_prior_group_step(group, proof_target=proof_target, bridge=bridge)
        if (prior is not None and verified_db_step(prior, proof_target=proof_target, bridge=bridge)
                and type(prior.conclusion) is Relation
                and type(prior.conclusion.rhs) is FiniteCyclicGroup
                and prior.conclusion not in items):
            items.append(prior.conclusion)
        return tuple(items)

    def expand(goal):
        if (type(goal) is not CyclicStructureStatement or type(goal.group) is not TodaPrimaryGroup
                or type(goal.order) is not int or goal.order < 2
                or type(proof_target) is not Relation
                or proof_target.relation_type is not RelationType.EQUALITY
                or proof_target.lhs != goal.group
                or proof_target.rhs != FiniteCyclicGroup(goal.order, goal.generator)):
            return ()
        b = goal.group
        q, n = b.group_dimension, b.sphere_dimension
        if type(q) is not int or type(n) is not int or n < 3 or q <= n:
            return ()
        a, c = TodaPrimaryGroup(q-1, n-1), TodaPrimaryGroup(q+1, 2*n-1)
        delta = TodaDeltaMap(c, a)
        signed = []
        for link in bridge.proof_links:
            step = link.step
            claim = None if step is None else step.conclusion
            if (type(claim) is TodaDeltaImageUpToSignStatement and claim.map == delta
                    and type(claim.positive_value) is Multiple
                    and len(linked_cited_steps(bridge, claim)) == 1 and claim not in signed):
                signed.append(claim)
        if not signed:
            return ()
        options = []
        for middle in presentations(a):
            for source in presentations(c):
                image = GeneratorImage(TodaSuspensionMap(a,b), middle.rhs.generator, goal.generator)
                for claim in signed:
                    for option in expand_finite_cyclic_quotient(goal, middle, source, claim, image, bridge=bridge):
                        if not any(old.subgoals == option.subgoals for old in options):
                            options.append(option)
        return tuple(options)

    return expand
