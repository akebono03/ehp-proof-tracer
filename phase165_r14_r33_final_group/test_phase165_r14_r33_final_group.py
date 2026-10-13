from dataclasses import replace
from pathlib import Path
import pytest
from proof import ProofRule
from homotopy_groups import TodaPrimaryGroup,FreeCyclicGroup
from hopf_facts import ETA_2
from phase165_r14_r33_final_group import (
    pi33_cyclic_step,hopf_eta2_image_step,derive_final_group_from_steps,
    derive_adopted_tex_final_group,audit_r33)

TEX=Path(__file__).with_name("toda_51_complete.tex")

def test_source_group_from_adopted_tex():
    assert pi33_cyclic_step(TEX).conclusion.lhs==TodaPrimaryGroup(3,3)

def test_generator_image_from_existing_prop51():
    assert hopf_eta2_image_step().conclusion.source_generator==ETA_2

def test_final_relation_derived_from_three_steps():
    iso,diagonal,image,final=derive_adopted_tex_final_group(TEX)
    assert final.conclusion.lhs==TodaPrimaryGroup(3,2)
    assert final.conclusion.rhs==FreeCyclicGroup(ETA_2)
    assert final.rule is ProofRule.INFERENCE
    assert final.premises==(iso,diagonal,image)

def test_incorrect_target_group_rejected():
    iso,diagonal,image,_=derive_adopted_tex_final_group(TEX)
    bad=replace(diagonal,conclusion=replace(diagonal.conclusion,lhs=TodaPrimaryGroup(4,4)))
    with pytest.raises(ValueError):derive_final_group_from_steps(iso,bad,image)

def test_incorrect_generator_rejected():
    iso,diagonal,image,_=derive_adopted_tex_final_group(TEX)
    bad=replace(image,conclusion=replace(image.conclusion,target_generator=ETA_2))
    with pytest.raises(ValueError):derive_final_group_from_steps(iso,diagonal,bad)

def test_wrong_iso_map_rejected():
    iso,diagonal,image,_=derive_adopted_tex_final_group(TEX)
    bad=replace(iso,conclusion=replace(iso.conclusion,map=object()))
    with pytest.raises(ValueError):derive_final_group_from_steps(bad,diagonal,image)

def test_final_audit_keeps_citation_boundary():
    r=audit_r33(TEX)
    assert r["final_proof_step_created"]
    assert not r["strict_registry_citation_approved"]
    assert not r["production_pi32_proved"]
