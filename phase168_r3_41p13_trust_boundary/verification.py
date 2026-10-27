"""Validate a searched proof tree before a positioned Web narrative handoff.

This is a gateway for the canonical searched/screened path, not a generic
proof checker for arbitrary user-defined inference rule implementations.
No certificate flag is written to PartialProofResult or ProofNarrativeModel.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from unified_statement_registry import AssertionOrigin


class UnverifiedProofTree(ValueError):
    """A proposed proof tree has no valid screened and positioned derivation."""


def verify_proof_tree_for_narrative(
    result: PartialProofResult,
    bridge: RegistryBridgeResult,
    *,
    citing_assertion_id: str | None,
    derived_target_without_citing_id: bool = False,
) -> tuple[int, int]:
    """Check source leaves and replay existing inference matches, or reject.

    The citing ID must be resolved from the unscreened registered goal, not
    constructed from a displayed group label. The supplied bridge must be the
    screened bridge actually used by canonical backward search.

    All nested premises are visited, including premises of earlier internal
    proofs. Neither the result nor the bridge is modified. The result is only
    a count for diagnostics and MUST NOT be treated as a transferable seal.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if derived_target_without_citing_id:
        if citing_assertion_id is not None:
            raise ValueError("derived-target mode requires no citing assertion")
        if result.status is not ProofSearchStatus.COMPLETE:
            raise ValueError("derived-target mode requires a completed proof")
        if not any(
            step.rule is ProofRule.INFERENCE
            and step.conclusion == result.conclusion
            for step in result.proven_steps
        ):
            raise UnverifiedProofTree("an uncited goal must be independently inferred")
    else:
        if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
            raise ValueError("citing_assertion_id must identify a positioned goal")
        bridge.registry.assertion(citing_assertion_id)

    def _same_group_as_derived_target(source: object, target: object) -> bool:
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from proof import Relation
        source_group = (
            source.group if isinstance(source, TodaPrimaryGroupZeroStatement)
            else source.lhs if isinstance(source, Relation) else None
        )
        target_group = (
            target.group if isinstance(target, TodaPrimaryGroupZeroStatement)
            else target.lhs if isinstance(target, Relation) else None
        )
        return source_group is not None and source_group == target_group

    checked: set[int] = set()
    active: set[int] = set()
    inference_count = 0
    given_count = 0

    def visit(step: ProofStep) -> None:
        nonlocal inference_count, given_count
        if not isinstance(step, ProofStep):
            raise UnverifiedProofTree("a proof premise is not a ProofStep")
        identity = id(step)
        if identity in checked:
            return
        if identity in active:
            raise UnverifiedProofTree("cyclic proof ancestry")
        active.add(identity)
        try:
            if step.rule is ProofRule.GIVEN:
                if step.premises:
                    raise UnverifiedProofTree("GIVEN has unproved premises")
                # R10E4: the DB assumption is authenticated by a fresh
                # exact-row read and the target-dependent lexicographic gate.
                # It is NOT promoted to a Toda FIXED_STATEMENT.
                from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step
                accepted = verified_db_step(
                    step, proof_target=result.conclusion, bridge=bridge,
                )
                for link in bridge.proof_links:
                    if link.step is None or link.step != step:
                        continue
                    assertion = bridge.registry.assertion(link.assertion_id)
                    if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                            and type(assertion.content) is type(step.conclusion)
                            and assertion.content == step.conclusion
                            and (
                                (
                                    derived_target_without_citing_id
                                    and bridge.registry.reference(
                                        assertion.reference_id
                                    ).publication_position is not None
                                    and assertion.content != result.conclusion
                                    and not _same_group_as_derived_target(
                                        assertion.content, result.conclusion
                                    )
                                )
                                or (
                                    not derived_target_without_citing_id
                                    and precedes_citing_assertion(
                                        bridge, link.assertion_id,
                                        citing_assertion_id,
                                    )
                                )
                            )):
                        accepted = True
                        break
                if not accepted:
                    raise UnverifiedProofTree("GIVEN is not screened, fixed and prior")
                given_count += 1
            elif step.rule is ProofRule.INFERENCE:
                if not isinstance(step.inference_rule, InferenceRule):
                    raise UnverifiedProofTree("inference has no typed rule")
                for premise in step.premises:
                    visit(premise)
                try:
                    matches = find_inference_matches_for_rule(
                        step.inference_rule, step.premises
                    )
                    accepted = any(
                        len(match.premises) == len(step.premises)
                        and all(a is b for a, b in zip(match.premises, step.premises))
                        and type(derived.conclusion) is type(step.conclusion)
                        and derived.conclusion == step.conclusion
                        for match in matches
                        for derived in (apply_inference_match(match),)
                    )
                except (TypeError, ValueError, AttributeError, IndexError) as exc:
                    raise UnverifiedProofTree("inference replay failed") from exc
                if not accepted:
                    raise UnverifiedProofTree("inference has no matching derivation")
                inference_count += 1
            else:
                raise UnverifiedProofTree("unsupported proof-step origin")
            checked.add(identity)
        finally:
            active.remove(identity)

    for step in result.proven_steps:
        visit(step)
    if result.status is ProofSearchStatus.COMPLETE:
        if result.conclusion is None or not any(
            type(step.conclusion) is type(result.conclusion)
            and step.conclusion == result.conclusion for step in result.proven_steps
        ):
            raise UnverifiedProofTree("completed proof has no matching conclusion")
        # A proof of another group cannot be certified for this result.target.
        # Source chronology and inference matching alone do not bind the target.
        # Preserve the historical generic checker for non-group synthetic input;
        # canonical Web search always supplies a typed group conclusion.
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from proof import Relation, RelationType

        if isinstance(result.conclusion, Relation):
            if (result.conclusion.relation_type is not RelationType.EQUALITY
                    or result.conclusion.lhs != result.target):
                raise UnverifiedProofTree("completed proof target does not match group")
        elif isinstance(result.conclusion, TodaPrimaryGroupZeroStatement):
            if result.conclusion.group != result.target:
                raise UnverifiedProofTree("completed zero proof target does not match group")
    return inference_count, given_count
