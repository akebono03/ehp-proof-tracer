from dataclasses import replace
import pytest
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r25_prop42_review import (
    CANDIDATE_IDS,inspect_prop42_sources,audit_r25,render_report,
)

def test_candidate_texts_exported_in_full():
    bridge,_=build_phase165_r5_manifest_bridge()
    rows=inspect_prop42_sources(bridge)
    assert tuple(r.assertion_id for r in rows)==CANDIDATE_IDS
    assert all(r.source_text_present and r.source_text for r in rows)

def test_candidate_review_does_not_falsely_certify():
    bridge,_=build_phase165_r5_manifest_bridge()
    assert all(not r.certified for r in inspect_prop42_sources(bridge))

def test_report_contains_both_raw_sources():
    report=audit_r25()
    rendered=render_report(report)
    assert all(row["source_text"] in rendered for row in report["source_reviews"])

def test_review_remains_read_only():
    bridge,_=build_phase165_r5_manifest_bridge()
    before=(len(bridge.registry._assertions),len(bridge.proof_links))
    inspect_prop42_sources(bridge)
    assert before==(len(bridge.registry._assertions),len(bridge.proof_links))

def test_missing_source_candidate_fails_closed():
    bridge,_=build_phase165_r5_manifest_bridge()
    saved=bridge.registry._assertions.pop(CANDIDATE_IDS[0])
    try:
        with pytest.raises(ValueError,match="missing recorded"):
            inspect_prop42_sources(bridge)
    finally:
        bridge.registry._assertions[CANDIDATE_IDS[0]]=saved

def test_target_window_not_approved():
    report=audit_r25()
    assert report["candidate_count"]==2
    assert report["new_proof_steps"]==0
    assert not report["semantic_application_certified"]
