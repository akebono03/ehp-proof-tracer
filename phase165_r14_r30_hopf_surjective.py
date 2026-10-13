"""R14-R30: derive H surjectivity from R29 and Proposition 4.2 (4.4).

Uses the adopted-TeX n=1 interpretation; strict citation status is unchanged.
"""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import (
    TodaPrimaryGroup, TodaHopfInvariantMap, TodaEHPExactnessWindow,
)
from map_facts import EHP_H_MAP, EHP_DELTA_MAP
from phase165_r14_r29_delta_derived import (
    Prop42ApplicationPolicy, derive_adopted_tex_delta_zero,
)
from phase165_r14_r26_prop42_typed import bind_proposition42, validate_prop42_source
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r9_ehp_exactness import (
    hopf_surjective_from_exactness_rule, expand_generic_ehp_hopf_goal,
)
from phase165_r14_r6_generic_iso import MapSurjective
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofStep, ProofRule, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def pi32_hopf_surjectivity_goal() -> MapSurjective:
    return MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(3, 2), TodaPrimaryGroup(3, 3),
    ))


def prop42_h_delta_exactness_step(policy: Prop42ApplicationPolicy) -> ProofStep:
    """Specialize (4.4) to pi3^2 -> pi3^3 -> pi1^1, not Delta->E."""
    if not isinstance(policy, Prop42ApplicationPolicy):
        raise TypeError("application policy required")
    if not policy.use_unrestricted_statement_as_written or policy.chapter_wide_exclusion_found:
        raise ValueError("n=1 scope is not accepted")
    bridge, _ = build_phase165_r5_manifest_bridge()
    validate_prop42_source(bridge)
    # n=1,i=2 yields H: pi3^2 -> pi3^3 ->Delta pi1^1.
    binding = bind_proposition42(bridge, n=1, i=2, index_scope_confirmed=True)
    delta_e_window = binding.typed_statement.window
    window = TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(3, 2),
        middle_term=delta_e_window.source_term,
        target_term=delta_e_window.middle_term,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
    )
    return ProofStep(
        conclusion=TodaProp42ExactnessStatement(window),
        premises=(),
        rule=ProofRule.GIVEN,
    )


def derive_hopf_surjectivity_from_steps(
    delta_zero_step: ProofStep, exactness_step: ProofStep,
) -> ProofStep:
    """Invoke the existing general EHP inference matcher and factory."""
    if not isinstance(delta_zero_step, ProofStep) or not isinstance(exactness_step, ProofStep):
        raise TypeError("both premises must be ProofSteps")
    goal = pi32_hopf_surjectivity_goal()
    expansions = expand_generic_ehp_hopf_goal(goal)
    if len(expansions) != 1:
        raise ValueError("expected one general EHP surjectivity expansion")
    expansion = expansions[0]
    if (delta_zero_step.conclusion, exactness_step.conclusion) != expansion.subgoals:
        raise ValueError("premises do not match H->Delta exactness window")
    rule = hopf_surjective_from_exactness_rule()
    matches = find_inference_matches_for_rule(rule, (delta_zero_step, exactness_step))
    if len(matches) != 1:
        raise ValueError("EHP premise matching failed")
    derived = derive_inference_proof_step(matches[0])
    if derived.conclusion != goal or derived.rule is not ProofRule.INFERENCE:
        raise ValueError("surjectivity inference failed")
    if len(derived.premises) != 2:
        raise ValueError("provenance premises lost")
    return derived


def derive_adopted_tex_hopf_surjectivity(tex_path: Path, policy: Prop42ApplicationPolicy):
    iso, delta_e, delta_zero = derive_adopted_tex_delta_zero(Path(tex_path), policy)
    h_delta = prop42_h_delta_exactness_step(policy)
    surjective = derive_hopf_surjectivity_from_steps(delta_zero, h_delta)
    return iso, delta_e, delta_zero, h_delta, surjective


def audit_r30(tex_path: Path) -> dict:
    policy = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)
    iso, delta_e, delta_zero, h_delta, surjective = derive_adopted_tex_hopf_surjectivity(tex_path, policy)
    return {
        "phase": "165 R14-R30",
        "prop42_source": "phase163:archive:toda:tex:ch4:0005",
        "scope_policy": "GENERAL_STATEMENT_AS_WRITTEN_N1_WITH_NO_KNOWN_EXCLUSION",
        "r29_delta_zero_reused": delta_zero.rule is ProofRule.INFERENCE,
        "h_delta_exactness": repr(h_delta.conclusion),
        "h_surjective_goal": repr(surjective.conclusion),
        "h_surjective_proof_step_created": True,
        "h_surjective_rule": surjective.rule.value,
        "h_surjective_premises": len(surjective.premises),
        "strict_registry_citation_approved": False,
        "pi32_proved": False,
        "full_pytest_run": False,
        "status": "ADOPTED_TEX_HOPF_SURJECTIVE_DERIVED_STRICT_CITATION_PENDING",
    }
