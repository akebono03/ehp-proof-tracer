"""Phase 162 R4-B2: construct concrete Toda (4.5) proof ancestry.

Do not normalize suspended generators or replace a repository root.
"""

from dataclasses import dataclass

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import ProofStep, Relation, RelationType, run_inference_until_stable_with_history
from toda_group_result import TodaGroupResult
from toda_stable_group_transport import toda_45_generic_finite_cyclic_transport_inference_rule
from toda_stable_proof_path_selection import (
    TodaStableProofPathKind,
    select_toda_stable_proof_path,
)
from toda_stable_transport import build_canonical_toda_45_isomorphism_step


@dataclass(frozen=True)
class TodaStableConcreteTransportProof:
    target: TodaPrimaryGroup
    base_step: ProofStep
    isomorphism_step: ProofStep
    transported_step: ProofStep


def build_toda_stable_concrete_transport_proof(
    target_result: TodaGroupResult,
    base_result: TodaGroupResult,
) -> TodaStableConcreteTransportProof:
    """Derive a concrete-target suspended group, preserving all rule premises.

    The suspended generator is deliberately *not* identified with a named
    eta-family element. That equality needs a separate checked derivation.
    """
    if not isinstance(target_result, TodaGroupResult):
        raise TypeError("target_result must be a TodaGroupResult")
    if not isinstance(base_result, TodaGroupResult):
        raise TypeError("base_result must be a TodaGroupResult")

    selection = select_toda_stable_proof_path(target_result)
    if selection.kind is not TodaStableProofPathKind.STABLE_TODA45_TRANSPORT:
        raise ValueError("target must be stable and strictly above its base")
    if base_result.target != selection.base:
        raise ValueError("base_result target does not match the canonical stable base")

    base_step = base_result.proof_step
    statement = base_step.conclusion
    if (
        not isinstance(statement, Relation)
        or statement.relation_type != RelationType.EQUALITY
        or statement.lhs != selection.base
        or not isinstance(statement.rhs, FiniteCyclicGroup)
    ):
        raise ValueError("base proof must conclude a finite-cyclic group equality")

    iso_step = build_canonical_toda_45_isomorphism_step(selection.target)
    inference_rule = toda_45_generic_finite_cyclic_transport_inference_rule()
    result = run_inference_until_stable_with_history(
        inference_rule,
        (base_step, iso_step),
    )
    matches = tuple(
        step for step in result.steps
        if step.inference_rule is inference_rule
        and len(step.premises) == 2
        and step.premises[0] is base_step
        and step.premises[1] is iso_step
    )
    if len(matches) != 1:
        raise ValueError("expected exactly one transport derivation from base and (4.5)")

    return TodaStableConcreteTransportProof(
        target=selection.target,
        base_step=base_step,
        isomorphism_step=iso_step,
        transported_step=matches[0],
    )
