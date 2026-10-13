"""R14-R31: derive H injectivity from Toda (5.1) and E->H exactness."""
from __future__ import annotations
from pathlib import Path

from homotopy_groups import (
    TodaPrimaryGroup,TodaPrimaryGroupZeroStatement,TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
)
from map_facts import EHP_E_MAP,EHP_H_MAP
from phase165_r14_r2_toda51 import TODA_51_SCHEMAS,instantiate_toda51_clause
from phase165_r14_r21_toda51_completion import complete_toda51_source
from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy
from phase165_r14_r26_prop42_typed import bind_proposition42,validate_prop42_source
from phase165_r14_r9_ehp_exactness import (
    hopf_injective_from_exactness_rule,expand_generic_ehp_hopf_goal,
)
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofStep,ProofRule,find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement

def pi32_hopf_injective_goal() -> MapInjective:
    return MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(3,2),TodaPrimaryGroup(3,3)))

def toda51_pi21_zero_step(tex_path:Path) -> ProofStep:
    """Make the concrete zero statement from the adopted (5.1) text."""
    source=complete_toda51_source(Path(tex_path).read_text(encoding="utf-8"))
    if source.clauses[0].key!="pi1_zero":
        raise ValueError("Toda (5.1) zero clause absent")
    claim=instantiate_toda51_clause(TODA_51_SCHEMAS[0],2)
    if claim.lhs!=TodaPrimaryGroup(2,1) or claim.rhs!=0:
        raise ValueError("Toda (5.1) specialization mismatch")
    return ProofStep(
        conclusion=TodaPrimaryGroupZeroStatement(claim.lhs),
        premises=(),rule=ProofRule.GIVEN,
    )

def prop42_e_h_exactness_step(policy:Prop42ApplicationPolicy) -> ProofStep:
    if not isinstance(policy,Prop42ApplicationPolicy):
        raise TypeError("policy required")
    if not policy.use_unrestricted_statement_as_written or policy.chapter_wide_exclusion_found:
        raise ValueError("n=1 is not approved")
    bridge,_=build_phase165_r5_manifest_bridge()
    validate_prop42_source(bridge)
    binding=bind_proposition42(bridge,n=1,i=2,index_scope_confirmed=True)
    w=binding.typed_statement.window
    return ProofStep(
        conclusion=TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
            source_term=TodaPrimaryGroup(2,1),
            middle_term=TodaPrimaryGroup(3,2),
            target_term=w.source_term,
            first_map=EHP_E_MAP,
            second_map=EHP_H_MAP,
        )),
        premises=(),rule=ProofRule.GIVEN,
    )

def derive_hopf_injectivity_from_steps(
    zero_step:ProofStep,exactness_step:ProofStep,
) -> ProofStep:
    if not isinstance(zero_step,ProofStep) or not isinstance(exactness_step,ProofStep):
        raise TypeError("two ProofSteps required")
    goal=pi32_hopf_injective_goal()
    expansions=expand_generic_ehp_hopf_goal(goal)
    if len(expansions)!=1:
        raise ValueError("no unique EHP injectivity rule")
    if (zero_step.conclusion,exactness_step.conclusion)!=expansions[0].subgoals:
        raise ValueError("premises do not match E->H exactness window")
    matches=find_inference_matches_for_rule(
        hopf_injective_from_exactness_rule(),(zero_step,exactness_step))
    if len(matches)!=1:
        raise ValueError("EHP matching failed")
    result=derive_inference_proof_step(matches[0])
    if (result.conclusion!=goal or result.rule is not ProofRule.INFERENCE
            or len(result.premises)!=2):
        raise ValueError("H injectivity derivation failed")
    return result

def derive_adopted_tex_hopf_injectivity(
    tex_path:Path,policy:Prop42ApplicationPolicy,
)->tuple[ProofStep,ProofStep,ProofStep]:
    zero=toda51_pi21_zero_step(tex_path)
    exact=prop42_e_h_exactness_step(policy)
    injective=derive_hopf_injectivity_from_steps(zero,exact)
    return zero,exact,injective

def audit_r31(tex_path:Path)->dict:
    policy=Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)
    zero,exact,injective=derive_adopted_tex_hopf_injectivity(tex_path,policy)
    return {
        "phase":"165 R14-R31",
        "toda51_zero_goal":repr(zero.conclusion),
        "prop42_e_h_exactness":repr(exact.conclusion),
        "hopf_injective_goal":repr(injective.conclusion),
        "hopf_injective_proof_step_created":True,
        "hopf_injective_rule":injective.rule.value,
        "hopf_injective_premises":len(injective.premises),
        "strict_registry_citation_approved":False,
        "pi32_proved":False,
        "status":"ADOPTED_TEX_HOPF_INJECTIVE_DERIVED_STRICT_CITATION_PENDING",
        "full_pytest_run":False,
    }
