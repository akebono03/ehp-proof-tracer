"""R14-R18: derive diagonal E-isomorphism only from supplied certified group steps.

The foundational suspension proof is explicitly identified; this adapter does
not manufacture Toda literature leaves or approve Proposition 4.2.
"""
from __future__ import annotations

from homotopy_groups import TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r14_diagonal_and_prop42 import (
    diagonal_suspension_subgoals,
    diagonal_suspension_isomorphism_rule,
    review_prop42_scope,
)
from phase165_r14_r17_foundational_proofstep import derive_foundational_suspension_step
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import ProofStep, ProofRule, find_inference_matches_for_rule


class DiagonalEvidenceMissing(ValueError):
    """Required certified Toda group evidence is unavailable or mismatched."""


def derive_diagonal_iso_from_certified_groups(
    suspension: TodaSuspensionMap,
    source_group_step: ProofStep | None,
    target_group_step: ProofStep | None,
) -> ProofStep:
    """Use existing INFERENCE rule and R17 foundation, never fabricate group leaves.

    The caller is responsible for obtaining both group steps from an independently
    verified registry lookup. A bare typed assertion is insufficient.
    """
    subgoals = diagonal_suspension_subgoals(suspension)
    if subgoals is None:
        raise DiagonalEvidenceMissing("suspension is not a diagonal suspension")
    for step, goal in zip((source_group_step, target_group_step), subgoals[:2]):
        if not isinstance(step, ProofStep) or type(step.conclusion) is not type(goal) or step.conclusion != goal:
            raise DiagonalEvidenceMissing("certified group ProofStep missing or mismatched")
    foundational_step = derive_foundational_suspension_step(subgoals[2])
    if foundational_step is None or foundational_step.foundational_reference is None:
        raise DiagonalEvidenceMissing("foundational suspension identity not available")
    steps = (source_group_step, target_group_step, foundational_step)
    matches = tuple(match for match in find_inference_matches_for_rule(
        diagonal_suspension_isomorphism_rule(), steps)
        if len(match.premises) == 3
        and all(a is b for a, b in zip(match.premises, steps)))
    if len(matches) != 1:
        raise DiagonalEvidenceMissing("no unique diagonal group isomorphism inference")
    conclusion = derive_inference_proof_step(matches[0])
    expected = TodaSuspensionIsomorphismStatement(suspension)
    if conclusion.rule is not ProofRule.INFERENCE or conclusion.conclusion != expected:
        raise DiagonalEvidenceMissing("inference result mismatch")
    return conclusion


def audit_r18(bridge=None) -> dict:
    if bridge is None:
        bridge, _ = build_phase165_r5_manifest_bridge()
    from homotopy_groups import TodaPrimaryGroup
    suspension = TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    goals = diagonal_suspension_subgoals(suspension)
    reviews = review_prop42_scope(bridge)
    try:
        derive_diagonal_iso_from_certified_groups(suspension, None, None)
    except DiagonalEvidenceMissing:
        fail_closed = True
    else:
        fail_closed = False
    if not fail_closed:
        raise RuntimeError("uncertified diagonal conclusion admitted")
    return {
        "phase": "165 R14-R18",
        "diagonal_obligations": [repr(x) for x in goals],
        "foundational_step_available": derive_foundational_suspension_step(goals[2]) is not None,
        "verified_toda_group_steps_supplied": 0,
        "diagonal_iso_in_production": False,
        "fail_closed_on_missing_group_steps": fail_closed,
        "prop42_candidate_count": len(reviews),
        "prop42_source_texts": [{"assertion_id": x["assertion_id"], "source_text": x["source_text"]} for x in reviews],
        "prop42_semantics_certified": False,
        "new_toda_proof_steps": 0,
        "pi32_proved": False,
        "full_pytest_run": False,
        "status": "FOUNDATIONAL_STEP_CONNECTED_CONDITIONALLY_TODA_LEAVES_MISSING",
    }
