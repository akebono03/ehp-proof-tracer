"""Foundation-only step for suspension of sphere identities (R14-R17).

No Toda reference, no archive promotion, no hidden registry publication order.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r16_foundational_suspension import (
    FOUNDATIONAL_SUSPENSION_IDENTITY,
    instantiate_foundational_identity_suspension,
)
from proof import ProofRule, ProofStep


def derive_foundational_suspension_step(goal: object) -> ProofStep | None:
    """Supply a named foundational axiom ONLY for the exact identity suspension.

    A separate trusted foundational rule is intended to be a mathematical
    axiom, not a derived Toda citation or automatically approved source leaf.
    """
    if not isinstance(goal, GeneratorSuspension):
        return None
    suspension = goal.map
    if not isinstance(suspension, TodaSuspensionMap):
        return None
    source = suspension.source_group
    n = source.sphere_dimension
    if (type(n) is not int or n < 1 or
            source != TodaPrimaryGroup(n, n) or
            suspension.target_group != TodaPrimaryGroup(n + 1, n + 1)):
        return None
    claim = instantiate_foundational_identity_suspension(n)
    if goal != claim.statement:
        return None
    return ProofStep(
        conclusion=goal,
        premises=(),
        rule=ProofRule.GIVEN,
        note=claim.justification,
        foundational_reference=FOUNDATIONAL_SUSPENSION_IDENTITY,
    )


def audit_r17() -> dict:
    identity = instantiate_foundational_identity_suspension(1).statement
    step = derive_foundational_suspension_step(identity)
    if step is None or step.foundational_reference != FOUNDATIONAL_SUSPENSION_IDENTITY:
        raise RuntimeError("foundational step provenance invalid")
    return {
        "phase": "165 R14-R17",
        "foundational_identity_step_created": 1,
        "foundational_rule": step.rule.value,
        "foundational_reference": step.foundational_reference.key,
        "toda_literature_leaf_created": 0,
        "registered_proof_eligible_added": 0,
        "proposition42_semantics_certified": False,
        "proposition42_application_approved": False,
        "pi32_proved": False,
        "full_pytest_run": False,
        "status": "FOUNDATIONAL_STEP_WITH_EXPLICIT_PROVENANCE_NOT_REGISTERED_TODA_PROOF",
    }
