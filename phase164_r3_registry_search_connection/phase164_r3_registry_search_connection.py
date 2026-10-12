"""Phase 164 R3: guarded registry-to-Phase-161 pi_5^3 leaf connection.

This adapter does not certify mathematics, create ProofSteps, change search
rules, or automatically approve any catalog entry. Verified assertion IDs,
publication order, and exactness witnesses are independent caller evidence.
"""
from dataclasses import dataclass

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    ValidatedBackwardReconstruction,
    reconstruct_phase161_r7_validated_goal,
    validate_phase161_r7_provenance,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class RegisteredLiteraturePremise:
    assertion_id: str
    step: ProofStep


@dataclass(frozen=True)
class RegistrySearchInput:
    available_leaf_steps: tuple[ProofStep, ...]
    accepted_assertion_ids: tuple[str, ...]


def select_phase164_r3_pi5_3_leaves(
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
    literature_premises: tuple[RegisteredLiteraturePremise, ...],
    exactness_steps: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> RegistrySearchInput:
    """Fail closed unless both existing literature leaves are R2-eligible.

    A supplied ID is not proof of correctness. The exact typed conclusion,
    existing inference ancestry and R2 position safeguards must all agree.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(literature_premises, tuple) or any(
        not isinstance(item, RegisteredLiteraturePremise) for item in literature_premises
    ):
        raise TypeError("literature_premises must contain RegisteredLiteraturePremise")
    if not isinstance(exactness_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in exactness_steps
    ):
        raise TypeError("exactness_steps must be ProofStep tuple")
    if not isinstance(trusted_given_roots, tuple):
        raise TypeError("trusted_given_roots must be tuple")
    if len(literature_premises) != 2 or len(exactness_steps) != 4:
        raise ValueError("pi5_3 requires two literature premises and four exactness witnesses")

    steps = tuple(item.step for item in literature_premises)
    if any(step.rule is not ProofRule.INFERENCE for step in steps):
        raise ValueError("literature leaves must retain their INFERENCE ancestry")
    if any(
        step.rule is not ProofRule.GIVEN
        or step.premises
        or not isinstance(step.conclusion, TodaProp42ExactnessStatement)
        for step in exactness_steps
    ):
        raise ValueError("exactness witnesses must be independent GIVEN steps")
    if len({id(step) for step in steps + exactness_steps}) != 6:
        raise ValueError("duplicate proof step identity")
    identifiers = tuple(item.assertion_id for item in literature_premises)
    if len(set(identifiers)) != 2:
        raise ValueError("duplicate assertion binding")

    for item in literature_premises:
        entry = bridge.registry.assertion(item.assertion_id)
        # Identity of the mathematical statement is checked structurally; the
        # Assertion ID by itself cannot authorize an unrelated ProofStep.
        if type(entry.content) is not type(item.step.conclusion):
            raise ValueError("registered conclusion type mismatch")
        equality = entry.content == item.step.conclusion
        if type(equality) is not bool or not equality:
            raise ValueError("registered conclusion mismatch")
        decision = assess_phase164_r2_citation(
            bridge, item.assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if not decision.usable:
            raise ValueError(
                f"citation not eligible: {item.assertion_id}: "
                f"{decision.status.value}/{decision.reason}"
            )

    leaves = steps + exactness_steps
    validate_phase161_r7_provenance(leaves, trusted_given_roots)
    return RegistrySearchInput(leaves, identifiers)


def reconstruct_phase164_r3_pi5_3(
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
    literature_premises: tuple[RegisteredLiteraturePremise, ...],
    exactness_steps: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> ValidatedBackwardReconstruction:
    """Invoke unchanged Phase 161 R7 only after registry-backed screening."""
    selected = select_phase164_r3_pi5_3_leaves(
        bridge, citing_assertion_id, literature_premises, exactness_steps,
        trusted_given_roots, verified_assertion_ids=verified_assertion_ids,
    )
    return reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), selected.available_leaf_steps,
        trusted_given_roots,
    )
