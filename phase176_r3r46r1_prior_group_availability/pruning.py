"""Reject zero obligations using eligible nonzero evidence, without proof insertion."""
from __future__ import annotations

from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
    TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
)
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin

TYPED_MODES = ('typed_reference', 'typed_reference_ordered', 'typed_reference_publication')


def nonzero_presentation(statement, group):
    """Only supported concrete, nontrivial group presentations contradict zero."""
    if (type(group) is not TodaPrimaryGroup
            or type(group.group_dimension) is not int
            or type(group.sphere_dimension) is not int
            or group.sphere_dimension < 2
            or group.group_dimension < group.sphere_dimension
            or type(statement) is not Relation
            or statement.relation_type is not RelationType.EQUALITY
            or statement.lhs != group):
        return False

    def nontrivial(part):
        return (type(part) is FreeCyclicGroup
                or (type(part) is FiniteCyclicGroup
                    and type(part.order) is int and part.order > 1))

    structure = statement.rhs
    return (nontrivial(structure)
            or (type(structure) is DirectSumGroup
                and isinstance(structure.summands, tuple)
                and any(nontrivial(part) for part in structure.summands)))


def fixed_steps(bridge, statement, citing_id, lookup_mode, verified_assertion_ids):
    """Use exactly the solver's fixed-reference eligibility, not the raw catalog."""
    if lookup_mode == 'typed_reference':
        from phase165_r3_recursive_search import _typed_reference_steps
        return _typed_reference_steps(bridge, statement)
    if lookup_mode == 'typed_reference_ordered':
        from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps
        return ordered_typed_reference_steps(
            bridge, statement, citing_id, verified_assertion_ids=verified_assertion_ids,
        )
    if lookup_mode != 'typed_reference_publication':
        return ()
    from phase166_r3c_publication_order import precedes_citing_assertion
    steps = []
    for assertion in bridge.registry._assertions.values():
        if (type(assertion.content) is not type(statement)
                or assertion.content != statement
                or not precedes_citing_assertion(bridge, assertion.assertion_id, citing_id)):
            continue
        links = tuple(link for link in bridge.proof_links
                      if link.assertion_id == assertion.assertion_id)
        if len(links) != 1 or links[0].step is None:
            continue
        step = links[0].step
        if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                or type(step.conclusion) is not type(statement)
                or step.conclusion != statement):
            raise ValueError('ordered reference has inconsistent ProofStep')
        steps.append(step)
    return tuple(steps)


def contradiction_witness(goal, *, bridge, citing_id, lookup_mode,
                          verified_assertion_ids, proof_target, solved=(),
                          completed_internal_proofs=()):
    """Find a nonzero witness without recursively proving another group.

    Direct eligible zero evidence and reusable exact zero proofs retain
    precedence. SourceBoundGoal is intentionally not unwrapped here. A raw
    DB row or a proposed expansion is never enough for rejection. A returned
    witness is diagnostic only; it is not inserted into the accepted tree.
    """
    if type(goal) is not TodaPrimaryGroupZeroStatement or lookup_mode not in TYPED_MODES:
        return None
    group = goal.group
    if (type(group) is not TodaPrimaryGroup
            or type(group.group_dimension) is not int
            or type(group.sphere_dimension) is not int
            or group.sphere_dimension < 2
            or group.group_dimension < group.sphere_dimension):
        return None
    # Preserve direct source priority and citation ambiguity semantics.
    if fixed_steps(bridge, goal, citing_id, lookup_mode, verified_assertion_ids):
        return None
    for _, step in solved:
        if isinstance(step, ProofStep) and type(step.conclusion) is type(goal) and step.conclusion == goal:
            return None
    if completed_internal_proofs:
        from phase165_r52_r17_internal_dependency import find_reusable_internal_proof
        if find_reusable_internal_proof(goal, proof_target, completed_internal_proofs) is not None:
            return None
    # Prefer an already accepted nonzero result, then eligible fixed sources.
    for _, step in solved:
        if (isinstance(step, ProofStep) and step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                and step.conclusion != proof_target and nonzero_presentation(step.conclusion, group)):
            return step
    for assertion in bridge.registry._assertions.values():
        statement = assertion.content
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or statement == proof_target or not nonzero_presentation(statement, group)):
            continue
        evidence = fixed_steps(bridge, statement, citing_id, lookup_mode, verified_assertion_ids)
        if len(evidence) == 1 and not evidence[0].premises:
            return evidence[0]
    # The existing admission policy is the authority; no Toda (5.2)
    # re-derivation or independent proof of an adopted DB prior is needed.
    prior = admitted_prior_group_step(group, proof_target=proof_target, bridge=bridge)
    if prior is not None and nonzero_presentation(prior.conclusion, group):
        return prior
    return None
