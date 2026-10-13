from phase165_r14_r13_source_review import (
    collect_prop42_source_reviews, diagonal_suspension_requirements, audit_r13,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


def test_source_candidates_remain_separate():
    bridge, _ = build_phase165_r5_manifest_bridge()
    reviews = collect_prop42_source_reviews(bridge)
    assert len(reviews) == 2
    assert len({x.assertion_id for x in reviews}) == 2


def test_source_text_preserved_without_promotion():
    bridge, _ = build_phase165_r5_manifest_bridge()
    for item in collect_prop42_source_reviews(bridge):
        archived = bridge.registry.assertion(item.assertion_id).content["source_text"]
        assert item.source_text == archived
        assert item.typed_specialization_verified is False
        assert item.proof_eligible is False


def test_diagonal_requirements_are_explicit():
    result = diagonal_suspension_requirements()
    assert len(result["requirements"]) == 4
    assert "E(iota_1) = iota_2" in result["requirements"]
    assert result["certified"] is False


def test_read_only_registry_contract():
    bridge, _ = build_phase165_r5_manifest_bridge()
    initial = (len(bridge.registry._assertions), len(bridge.proof_links))
    report = audit_r13(bridge)
    assert initial == (len(bridge.registry._assertions), len(bridge.proof_links))
    assert report["source_review_count"] == 2


def test_no_false_proof_eligibility():
    report = audit_r13()
    assert report["proof_steps_created"] == 0
    assert report["mathematical_semantics_certified"] is False
    assert report["pi32_proved"] is False
    assert not report["proposition42_single_clause_selected"]
