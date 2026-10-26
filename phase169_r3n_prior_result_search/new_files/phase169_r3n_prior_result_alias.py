"""Connect a prior fixed group result to its registered DB presentation.

This module does not require, fetch, validate or replay an earlier group's proof.
It neither upgrades an archive/DB row into a GIVEN nor extends publication order.
Only an already screened, prior FIXED_STATEMENT ProofStep can be its premise.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from proof import (
    InferenceRule, PremisePattern, ProofRule, ProofStep,
    Relation, RelationType, find_inference_matches_for_rule,
)


def prior_result_presentation_rule(source: Relation, target: Relation) -> InferenceRule:
    """Require an explicit fixed source and a strict HyoujiGen presentation match."""
    if not (isinstance(source, Relation) and isinstance(target, Relation)
            and source.relation_type is RelationType.EQUALITY
            and target.relation_type is RelationType.EQUALITY
            and source.lhs == target.lhs
            and source != target):
        raise ValueError("distinct equal-group presentations are required")

    def guard(premises, bindings):
        if len(premises) != 1:
            return False
        step = premises[0]
        if step.rule is not ProofRule.GIVEN or step.conclusion != source:
            return False
        from phase168_r2_8_3_generator_identity.identity import (
            same_registered_group_presentation,
        )
        return same_registered_group_presentation(source.rhs, target.rhs)

    return InferenceRule(
        name="prior literature group result in registered generator presentation",
        description=(
            "Use an earlier, citation-screened fixed group result under "
            "the same fully registered HyoujiGen generator identity."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=target,
    )


def resolve_prior_result_alias_step(
    target: object,
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
) -> ProofStep | None:
    """Use DB results only after unique prior-source and screened-leaf checks.

    Exact fixed references are handled by the existing solver first. This
    function connects only a differing textual/structural presentation whose
    group and full generator factor identity are already registered. It never
    consults a previous proof's completion status.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
        raise ValueError("citing_assertion_id must be provided")
    if not (isinstance(target, Relation)
            and target.relation_type is RelationType.EQUALITY
            and isinstance(target.lhs, TodaPrimaryGroup)):
        return None
    n = target.lhs.sphere_dimension
    m = target.lhs.group_dimension
    if (type(n) is not int or type(m) is not int or n < 2 or m < n):
        return None
    source = resolve_prior_group_result(
        bridge,
        source_n=n,
        source_k=m - n,
        citing_assertion_id=citing_assertion_id,
    )
    if not source.eligible or source.relation is None:
        return None
    # The caller has already checked for exact screened GIVEN leaves.
    # The DB value may match the target while the fixed literature alias does not.
    from phase168_r2_8_3_generator_identity.identity import (
        same_registered_group_presentation,
    )
    if (target.lhs != source.relation.lhs
            or not same_registered_group_presentation(
                target.rhs, source.relation.rhs,
            )):
        return None
    assert source.source_assertion_id is not None
    assertion = bridge.registry.assertion(source.source_assertion_id)
    from unified_statement_registry import AssertionOrigin
    if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or not isinstance(assertion.content, Relation)
            or assertion.content.lhs != target.lhs
            or assertion.content.relation_type is not RelationType.EQUALITY
            or not same_registered_group_presentation(
                assertion.content.rhs, target.rhs,
            )):
        return None
    steps = tuple(
        link.step for link in bridge.proof_links
        if link.assertion_id == source.source_assertion_id
        and link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
        and link.step.conclusion == assertion.content
    )
    if len(steps) != 1:
        return None
    rule = prior_result_presentation_rule(steps[0].conclusion, target)
    matches = find_inference_matches_for_rule(rule, steps)
    if len(matches) != 1:
        return None
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    derived = derive_inference_proof_step(matches[0])
    if derived.rule is not ProofRule.INFERENCE or derived.conclusion != target:
        raise ValueError("prior result alias produced an unexpected conclusion")
    return derived
