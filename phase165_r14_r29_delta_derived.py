"""R14-R29: derive Delta=0 using the existing R23, R24 and R26 logic.

The n=1 specialization is an explicit adopted-text interpretation, NOT a
claim that the original edition and all global chapter hypotheses were checked.
"""
from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r24_delta_connection import (
    derive_delta_zero_from_steps, reviewed_r23_isomorphism, pi32_delta_goal,
)
from phase165_r14_r26_prop42_typed import (
    bind_proposition42, adopted_tex_proofstep,
)
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class Prop42ApplicationPolicy:
    """Record the explicit adopted-TeX scope interpretation for n=1."""
    use_unrestricted_statement_as_written: bool = False
    chapter_wide_exclusion_found: bool = False
    original_edition_verified: bool = False


def derive_adopted_tex_delta_zero(
    toda51_tex_path: Path,
    policy: Prop42ApplicationPolicy,
) -> tuple[ProofStep, ProofStep, ProofStep]:
    """Combine real inference steps, refusing missing or contrary scope policy."""
    if not isinstance(policy, Prop42ApplicationPolicy):
        raise TypeError("application policy is required")
    if not policy.use_unrestricted_statement_as_written:
        raise ValueError("n=1 interpretation not accepted")
    if policy.chapter_wide_exclusion_found:
        raise ValueError("n=1 explicitly excluded by broader hypotheses")
    iso, bridge = reviewed_r23_isomorphism(Path(toda51_tex_path))
    binding = bind_proposition42(bridge, n=1, i=2, index_scope_confirmed=True)
    exactness = adopted_tex_proofstep(binding)
    delta = derive_delta_zero_from_steps(iso, exactness)
    if delta.conclusion != pi32_delta_goal() or delta.rule is not ProofRule.INFERENCE:
        raise ValueError("Delta inference failed")
    if len(delta.premises) != 2:
        raise ValueError("Delta inference did not retain both proof premises")
    return iso, exactness, delta


def audit_r29(toda51_tex_path: Path) -> dict:
    policy = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)
    iso, exactness, delta = derive_adopted_tex_delta_zero(toda51_tex_path, policy)
    return {
        "phase": "165 R14-R29",
        "prop42_source": "phase163:archive:toda:tex:ch4:0005",
        "scope_policy": "GENERAL_STATEMENT_AS_WRITTEN_N1_WITH_NO_KNOWN_EXCLUSION",
        "chapter_scope_independently_verified": False,
        "original_edition_verified": policy.original_edition_verified,
        "r23_iso_step_connected": iso.rule is ProofRule.INFERENCE,
        "prop42_exactness_typed": repr(exactness.conclusion),
        "delta_zero_goal": repr(delta.conclusion),
        "delta_zero_proof_step_created": True,
        "delta_rule": delta.rule.value,
        "delta_premise_count": len(delta.premises),
        "strict_registry_citation_approved": False,
        "pi32_proved": False,
        "status": "ADOPTED_TEX_DELTA_ZERO_DERIVED_STRICT_CITATION_PENDING",
        "full_pytest_run": False,
    }
