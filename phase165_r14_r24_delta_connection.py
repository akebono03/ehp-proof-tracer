"""R14-R24: connect the actual reviewed R23 isomorphism to existing R11 inference.

Proposition 4.2 is a mandatory separate proof premise. No source assertion is
accepted automatically and no synthetic premise is used in the production audit.
"""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r14_r13_source_review import collect_prop42_source_reviews
from phase165_r14_r21_toda51_completion import complete_toda51_source
from phase165_r14_r22_same_reference import integrate_toda51_into_existing_reference
from phase165_r14_r23_toda51_inference import (
    AdoptedTextReview, derive_reviewed_diagonal_iso,
    promote_diagonal_from_existing_reference,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofStep, find_inference_matches_for_rule
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement


def pi32_delta_goal() -> TodaDeltaZeroStatement:
    return TodaDeltaZeroStatement(
        TodaDeltaMap(TodaPrimaryGroup(3, 3), TodaPrimaryGroup(1, 1))
    )


def derive_delta_zero_from_steps(
    iso_step: ProofStep, exactness_step: ProofStep,
) -> ProofStep:
    """Apply existing EHP rule only to correctly typed, matching steps."""
    if not isinstance(iso_step, ProofStep) or not isinstance(exactness_step, ProofStep):
        raise TypeError("both premises must be ProofStep instances")
    if not isinstance(exactness_step.conclusion, TodaProp42ExactnessStatement):
        raise ValueError("a typed Proposition 4.2 exactness proof step is required")
    expansions = expand_delta_zero_from_suspension_iso(pi32_delta_goal())
    if len(expansions) != 1:
        raise ValueError("Delta goal has no unique EHP inference")
    expansion = expansions[0]
    if iso_step.conclusion != expansion.subgoals[0]:
        raise ValueError("suspension isomorphism does not match this Delta goal")
    if exactness_step.conclusion != expansion.subgoals[1]:
        raise ValueError("exactness window does not match this Delta goal")
    matches = find_inference_matches_for_rule(
        expansion.rule, (iso_step, exactness_step)
    )
    if len(matches) != 1:
        raise ValueError("exactness and isomorphism cannot derive Delta zero")
    derived = derive_inference_proof_step(matches[0])
    if derived.conclusion != pi32_delta_goal():
        raise ValueError("inference produced a different conclusion")
    return derived


def reviewed_r23_isomorphism(tex_path: Path):
    """Reuse R23 reviewed adopted-TeX proof, without relaxing strict citation."""
    text = Path(tex_path).read_text(encoding="utf-8")
    completed = complete_toda51_source(text)
    bridge, _ = build_phase165_r5_manifest_bridge()
    updated = integrate_toda51_into_existing_reference(bridge, text)
    review = AdoptedTextReview(
        complete_source_sha256=completed.source_sha256,
        diagonal_clause_checked=True,
        reviewer_note="Adopted TeX checked in R21/R23; original edition not verified",
    )
    reviewed, ids = promote_diagonal_from_existing_reference(updated.bridge, review)
    return derive_reviewed_diagonal_iso(reviewed, ids), bridge


def audit_r24(tex_path: Path) -> dict:
    iso_step, bridge = reviewed_r23_isomorphism(tex_path)
    goal = pi32_delta_goal()
    expansion = expand_delta_zero_from_suspension_iso(goal)[0]
    candidates = collect_prop42_source_reviews(bridge)
    if len(candidates) != 2:
        raise ValueError("expected two unselected Proposition 4.2 source candidates")
    return {
        "phase": "165 R14-R24",
        "r23_iso_step_connected": iso_step.conclusion == expansion.subgoals[0],
        "iso_inference_rule": iso_step.rule.value,
        "delta_goal": repr(goal),
        "exactness_goal": repr(expansion.subgoals[1]),
        "prop42_source_candidates": [
            {"assertion_id": c.assertion_id, "locator": c.locator,
             "source_text": c.source_text} for c in candidates
        ],
        "prop42_candidate_count": len(candidates),
        "prop42_application_certified": False,
        "matching_exactness_proofsteps": 0,
        "production_delta_zero_proved": False,
        "pi32_proved": False,
        "status": "R23_ISO_CONNECTED_TO_R11_PROP42_EXACTNESS_PENDING",
        "full_pytest_run": False,
    }
