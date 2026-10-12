from dataclasses import replace
import pytest

from phase165_r12_typed_binding import build_batch_typed_bindings
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


def test_batch_covers_all_117_records_without_promoting_proofs():
    bridge, _ = build_phase165_r5_manifest_bridge()
    result = build_batch_typed_bindings(bridge)
    assert len(result.records) == 117
    assert result.unique_candidates + result.ambiguous_candidates + result.unmatched == 117
    assert result.mathematically_typed == 0
    assert result.proof_eligible == 0
    assert all(not item.source.proof_eligible and item.proof_step is None
               for item in result.records)


def test_adopted_tex_integrity_and_order_are_preserved():
    bridge, _ = build_phase165_r5_manifest_bridge()
    result = build_batch_typed_bindings(bridge)
    positions = [(r.source.source_chapter, r.source.source_position)
                 for r in result.records]
    assert positions == sorted(positions)
    assert len({r.source.assertion_id for r in result.records}) == 117


def test_locator_match_remains_unverified():
    bridge, _ = build_phase165_r5_manifest_bridge()
    result = build_batch_typed_bindings(bridge)
    assert result.unique_candidates == 11
    assert result.ambiguous_candidates == 12
    assert result.unmatched == 94
    assert all("UNVERIFIED" in r.status for r in result.records
               if r.candidate_assertion_ids)


def test_corrupted_tex_is_rejected():
    bridge, _ = build_phase165_r5_manifest_bridge()
    assertion = next(a for a in bridge.registry._assertions.values()
                     if a.assertion_id.startswith("phase163:archive:"))
    modified = dict(assertion.content)
    modified["source_text"] = "incorrect source text"
    bridge.registry._assertions[assertion.assertion_id] = replace(assertion, content=modified)
    with pytest.raises(ValueError, match="integrity"):
        build_batch_typed_bindings(bridge)


def test_source_promotion_is_rejected():
    bridge, _ = build_phase165_r5_manifest_bridge()
    assertion = next(a for a in bridge.registry._assertions.values()
                     if a.assertion_id.startswith("phase163:archive:"))
    modified = dict(assertion.content)
    modified["proof_eligible"] = True
    bridge.registry._assertions[assertion.assertion_id] = replace(assertion, content=modified)
    with pytest.raises(ValueError, match="eligibility"):
        build_batch_typed_bindings(bridge)
