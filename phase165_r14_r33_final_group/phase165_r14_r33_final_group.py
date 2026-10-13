"""R14-R33: reverse free-cyclic transport along a proved Hopf isomorphism."""
from __future__ import annotations
from pathlib import Path
from homotopy_groups import TodaPrimaryGroup,FreeCyclicGroup
from hopf_facts import ETA_2,IOTA_3,ETA_2_HOPF_INVARIANT_FACT
from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy
from phase165_r14_r32_hopf_isomorphism import derive_adopted_tex_hopf_isomorphism
from phase165_r14_r6_generic_iso import MapIsomorphism,GeneratorImage
from phase165_r14_r21_toda51_completion import complete_toda51_source
from proof import (InferenceRule,PremisePattern,Relation,RelationType,ProofRule,ProofStep,
                   find_inference_matches_for_rule)
from phase164_r8_proofstep_factory import derive_inference_proof_step


def _valid_reverse(premises, bindings):
    iso,target,image=(p.conclusion for p in premises)
    return (iso.map==image.map
            and getattr(iso.map,"target_group",None)==target.lhs
            and getattr(iso.map,"source_group",None) is not None
            and target.relation_type is RelationType.EQUALITY
            and isinstance(target.rhs,FreeCyclicGroup)
            and target.rhs.generator==image.target_generator)


def _build_reverse(premises):
    iso,target,image=(p.conclusion for p in premises)
    return Relation(lhs=iso.map.source_group,
                    rhs=FreeCyclicGroup(generator=image.source_generator),
                    relation_type=RelationType.EQUALITY)


def reverse_free_cyclic_transport_rule():
    """Infer source group's generator from iso, target generator, and its image."""
    return InferenceRule(
        name="generic reverse free cyclic structure transport along isomorphism",
        premise_patterns=(PremisePattern(statement_type=MapIsomorphism),
                          PremisePattern(statement_type=Relation,relation_type=RelationType.EQUALITY),
                          PremisePattern(statement_type=GeneratorImage)),
        match_guard=_valid_reverse,
        conclusion_builder=_build_reverse,
    )


def pi33_cyclic_step(tex_path:Path)->ProofStep:
    source=complete_toda51_source(Path(tex_path).read_text(encoding="utf8"))
    if len(source.clauses)!=6 or source.clauses[3].key!="diagonal_cyclic":
        raise ValueError("Toda (5.1) diagonal missing")
    return ProofStep(conclusion=Relation(
        lhs=TodaPrimaryGroup(3,3),rhs=FreeCyclicGroup(IOTA_3)),
        premises=(),rule=ProofRule.GIVEN)


def hopf_eta2_image_step()->ProofStep:
    fact=ETA_2_HOPF_INVARIANT_FACT
    if (fact.expression!=ETA_2 or fact.value!=IOTA_3
            or fact.source.locator!="Proposition 5.1"):
        raise ValueError("Proposition 5.1 source fact mismatch")
    from homotopy_groups import TodaHopfInvariantMap
    return ProofStep(conclusion=GeneratorImage(
        TodaHopfInvariantMap(TodaPrimaryGroup(3,2),TodaPrimaryGroup(3,3)),
        ETA_2,IOTA_3),premises=(),rule=ProofRule.GIVEN)


def derive_final_group_from_steps(iso:ProofStep,diagonal:ProofStep,image:ProofStep)->ProofStep:
    if not all(isinstance(x,ProofStep) for x in (iso,diagonal,image)):
        raise TypeError("three ProofSteps required")
    matched=find_inference_matches_for_rule(reverse_free_cyclic_transport_rule(),
                                             (iso,diagonal,image))
    if len(matched)!=1:
        raise ValueError("inverse generator transport requires matching premises")
    result=derive_inference_proof_step(matched[0])
    goal=Relation(TodaPrimaryGroup(3,2),FreeCyclicGroup(ETA_2))
    if result.conclusion!=goal or result.rule is not ProofRule.INFERENCE:
        raise ValueError("unexpected generated group structure")
    return result


def derive_adopted_tex_final_group(tex_path:Path):
    policy=Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)
    _,_,iso=derive_adopted_tex_hopf_isomorphism(tex_path,policy)
    diagonal=pi33_cyclic_step(tex_path)
    image=hopf_eta2_image_step()
    return iso,diagonal,image,derive_final_group_from_steps(iso,diagonal,image)


def audit_r33(tex_path:Path)->dict:
    iso,diagonal,image,final=derive_adopted_tex_final_group(tex_path)
    return {"phase":"165 R14-R33", "h_isomorphism_step":iso.rule.value,
            "diagonal_locator":"(5.1)","image_locator":"Proposition 5.1",
            "goal":repr(final.conclusion), "final_proof_step_created":True,
            "final_rule":final.rule.value,"final_premises":len(final.premises),
            "strict_registry_citation_approved":False,
            "production_pi32_proved":False,
            "status":"ADOPTED_TEX_PI32_GROUP_DERIVED_STRICT_REGISTRY_PENDING",
            "full_pytest_run":False}
