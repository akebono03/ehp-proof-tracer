"""R14-R32: derive Hopf isomorphism from existing H mono and epi steps."""
from __future__ import annotations

from pathlib import Path

from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy
from phase165_r14_r30_hopf_surjective import derive_adopted_tex_hopf_surjectivity
from phase165_r14_r31_hopf_injective import derive_adopted_tex_hopf_injectivity
from phase165_r14_r6_generic_iso import (
    MapIsomorphism, expand_generic_iso_goal, map_isomorphism_rule,
)
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def derive_hopf_isomorphism_from_steps(
    injective_step: ProofStep, surjective_step: ProofStep,
) -> ProofStep:
    """Check premises exactly and apply the existing mono+epi rule."""
    if not isinstance(injective_step, ProofStep) or not isinstance(surjective_step, ProofStep):
        raise TypeError("both premises must be ProofSteps")
    inj = injective_step.conclusion
    surj = surjective_step.conclusion
    if (type(inj).__name__ != "MapInjective"
            or type(surj).__name__ != "MapSurjective"
            or inj.map != surj.map):
        raise ValueError("injectivity and surjectivity of the same map required")
    goal = MapIsomorphism(inj.map)
    expansions = expand_generic_iso_goal(goal)
    if (len(expansions) != 1
            or expansions[0].subgoals != (inj, surj)):
        raise ValueError("generic isomorphism goal expansion mismatch")
    matches = find_inference_matches_for_rule(
        map_isomorphism_rule(), (injective_step, surjective_step),
    )
    if len(matches) != 1:
        raise ValueError("generic isomorphism inference did not match")
    result = derive_inference_proof_step(matches[0])
    if (result.conclusion != goal or result.rule is not ProofRule.INFERENCE
            or result.premises != (injective_step, surjective_step)):
        raise ValueError("inference result or provenance mismatch")
    return result


def derive_adopted_tex_hopf_isomorphism(
    tex_path: Path, policy: Prop42ApplicationPolicy,
) -> tuple[ProofStep, ProofStep, ProofStep]:
    """Reconstruct both branches, never substitute synthetic premises."""
    _, _, _, _, surjective = derive_adopted_tex_hopf_surjectivity(tex_path, policy)
    _, _, injective = derive_adopted_tex_hopf_injectivity(tex_path, policy)
    iso = derive_hopf_isomorphism_from_steps(injective, surjective)
    return injective, surjective, iso


def audit_r32(tex_path: Path) -> dict:
    policy = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)
    inj, surj, iso = derive_adopted_tex_hopf_isomorphism(tex_path, policy)
    return {
        "phase": "165 R14-R32",
        "hopf_injective_step_reused": inj.rule is ProofRule.INFERENCE,
        "hopf_surjective_step_reused": surj.rule is ProofRule.INFERENCE,
        "hopf_isomorphism": repr(iso.conclusion),
        "hopf_isomorphism_proof_step_created": True,
        "hopf_isomorphism_rule": iso.rule.value,
        "hopf_isomorphism_premises": len(iso.premises),
        "strict_registry_citation_approved": False,
        "pi32_proved": False,
        "status": "ADOPTED_TEX_HOPF_ISOMORPHISM_DERIVED_STRICT_CITATION_PENDING",
        "full_pytest_run": False,
    }
