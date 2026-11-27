"""Discover one-fold finite cyclic suspension transport obligations, never proofs."""
from homotopy_groups import (
    FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r24_web_search_connection import finite_cyclic_suspension_transport_inference_rule
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from proof import Relation, RelationType


def finite_cyclic_presentation(statement):
    """Require an explicit finite nontrivial cyclic presentation with typed generator."""
    if (type(statement) is not Relation
            or statement.relation_type is not RelationType.EQUALITY
            or type(statement.lhs) is not TodaPrimaryGroup
            or type(statement.rhs) is not FiniteCyclicGroup
            or type(statement.rhs.order) is not int or statement.rhs.order < 2):
        return False
    group = statement.lhs
    q, n = group.group_dimension, group.sphere_dimension
    return (type(q) is int and type(n) is int and n >= 2 and q >= n
            and typed_endpoints(statement.rhs.generator) == (q, n))


def suspension_transport_inputs(goal, source):
    """Return the existing rule's three premises, not certified facts."""
    if not finite_cyclic_presentation(goal) or not finite_cyclic_presentation(source):
        return None
    # The original rule constructs a canonical unannotated equality.
    if goal != Relation(goal.lhs, goal.rhs):
        return None
    a, b = source.lhs, goal.lhs
    if (b != TodaPrimaryGroup(a.group_dimension + 1, a.sphere_dimension + 1)
            or source.rhs.order != goal.rhs.order):
        return None
    suspension = TodaSuspensionMap(a, b)
    return (source, TodaSuspensionIsomorphismStatement(suspension),
            GeneratorImage(suspension, source.rhs.generator, goal.rhs.generator))


def build_finite_cyclic_suspension_transport_provider(*, bridge, proof_target):
    """Root-scoped proposal discovery in an already screened source context.

    First consider positioned linked literature, then the existing exact DB
    prior admission gate. A candidate presentation is only a backward goal.
    No provider installs a proof or resolves either map obligation here.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError('typed registry bridge required')

    def expand(goal):
        if goal != proof_target or not finite_cyclic_presentation(goal):
            return ()
        b = goal.lhs
        if b.sphere_dimension < 3:
            return ()
        a = TodaPrimaryGroup(b.group_dimension - 1, b.sphere_dimension - 1)
        presentations = []
        for link in bridge.proof_links:
            step = link.step
            claim = None if step is None else step.conclusion
            if (finite_cyclic_presentation(claim) and claim.lhs == a
                    and step in linked_cited_steps(bridge, claim)
                    and claim not in presentations):
                presentations.append(claim)
        prior = admitted_prior_group_step(a, proof_target=proof_target, bridge=bridge)
        if (prior is not None
                and verified_db_step(prior, proof_target=proof_target, bridge=bridge)
                and prior.conclusion not in presentations):
            presentations.append(prior.conclusion)
        options = []
        for source in presentations:
            required = suspension_transport_inputs(goal, source)
            if required is not None and not any(o.subgoals == required for o in options):
                options.append(GoalExpansion(
                    finite_cyclic_suspension_transport_inference_rule(), required))
        return tuple(options)

    return expand
