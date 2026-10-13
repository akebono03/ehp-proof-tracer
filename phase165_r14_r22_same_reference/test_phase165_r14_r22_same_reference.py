from pathlib import Path
import pytest
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r22_same_reference import integrate_toda51_into_existing_reference
from unified_statement_registry import AssertionOrigin

TEX = Path(__file__).with_name("toda_51_complete.tex").read_text(encoding="utf-8")


def test_existing_reference_reused_and_count_constant():
    bridge,_ = build_phase165_r5_manifest_bridge()
    result=integrate_toda51_into_existing_reference(bridge,TEX)
    assert result.reference_id in bridge.registry._references
    assert len(result.bridge.registry._references)==len(bridge.registry._references)
    assert len(result.bridge.registry._assertions)==len(bridge.registry._assertions)+6


def test_six_clauses_keep_source_archive_origin():
    bridge,_ = build_phase165_r5_manifest_bridge()
    result=integrate_toda51_into_existing_reference(bridge,TEX)
    entries=[result.bridge.registry.assertion(aid) for aid in result.component_ids]
    assert all(e.origin is AssertionOrigin.SOURCE_ARCHIVE for e in entries)
    assert all(e.available_after_position is None for e in entries)
    assert all(not e.content["proof_eligible"] for e in entries)


def test_original_registry_unchanged():
    bridge,_ = build_phase165_r5_manifest_bridge()
    before=len(bridge.registry._assertions)
    integrate_toda51_into_existing_reference(bridge,TEX)
    assert len(bridge.registry._assertions)==before


def test_diagonal_is_typed_without_proof_promotion():
    bridge,_ = build_phase165_r5_manifest_bridge()
    result=integrate_toda51_into_existing_reference(bridge,TEX)
    diagonal=result.bridge.registry.assertion(result.component_ids[3])
    assert len(diagonal.content["typed_specializations"])==2
    assert diagonal.content["typed_specializations"][0].lhs.sphere_dimension==1
    assert diagonal.content["typed_specializations"][1].lhs.sphere_dimension==2
    assert result.bridge.proof_links==bridge.proof_links


def test_missing_clause_rejected():
    bridge,_ = build_phase165_r5_manifest_bridge()
    with pytest.raises(ValueError):
        integrate_toda51_into_existing_reference(bridge,TEX.replace(r"\iota=E^{\infty}\iota_n",""))


def test_duplicate_component_registration_rejected():
    bridge,_=build_phase165_r5_manifest_bridge()
    first=integrate_toda51_into_existing_reference(bridge,TEX)
    with pytest.raises(ValueError,match="already registered"):
        integrate_toda51_into_existing_reference(first.bridge,TEX)
