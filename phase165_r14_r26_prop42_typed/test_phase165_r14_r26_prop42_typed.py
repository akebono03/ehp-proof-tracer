import pytest
from dataclasses import replace
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r26_prop42_typed import (
    SOURCE_ID, validate_prop42_source, typed_delta_e_window,
    bind_proposition42, adopted_tex_proofstep, audit_r26
)
from homotopy_groups import TodaPrimaryGroup

def test_source_is_real_proposition():
    bridge,_=build_phase165_r5_manifest_bridge()
    assert "完全列" in validate_prop42_source(bridge)

def test_wrong_locator_cannot_be_used():
    bridge,_=build_phase165_r5_manifest_bridge()
    good=bridge.registry._assertions[SOURCE_ID]
    bridge.registry._assertions[SOURCE_ID]=replace(
        good,reference_id="phase163:archive:toda:(4.2)")
    try:
        with pytest.raises((ValueError, KeyError)):
            validate_prop42_source(bridge)
    finally:
        bridge.registry._assertions[SOURCE_ID]=good

def test_target_delta_e_indices():
    s=typed_delta_e_window(1,2).window
    assert s.source_term==TodaPrimaryGroup(3,3)
    assert s.middle_term==TodaPrimaryGroup(1,1)
    assert s.target_term==TodaPrimaryGroup(2,2)

def test_bad_indices_rejected():
    for n,i in ((0,2),(1,-1),(1,0),(True,2),(1,True)):
        with pytest.raises(ValueError):
            typed_delta_e_window(n,i)

def test_source_does_not_imply_index_scope():
    bridge,_=build_phase165_r5_manifest_bridge()
    binding=bind_proposition42(bridge)
    assert not binding.index_scope_confirmed
    assert not binding.proof_eligible_in_strict_search
    with pytest.raises(ValueError,match="index scope"):
        adopted_tex_proofstep(binding)

def test_explicit_scope_conditional_step():
    bridge,_=build_phase165_r5_manifest_bridge()
    binding=bind_proposition42(bridge,index_scope_confirmed=True)
    step=adopted_tex_proofstep(binding)
    assert step.conclusion==binding.typed_statement
    assert step.premises==()

def test_production_not_promoted():
    audit=audit_r26()
    assert audit["production_exactness_proofsteps"]==0
    assert not audit["n1_scope_confirmed"]
