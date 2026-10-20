"""Focused tests for Phase 166 R3-B.  Full pytest is intentionally not run."""
from dataclasses import replace
import json

import pytest

from phase163_r4_registry_bridge import build_registry_bridge
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding import connect_phase163_publication_order
from unified_statement_registry import LiteratureEntry


def test_reuses_all_108_manifest_reference_positions_without_recomputing_order():
    bridge = build_registry_bridge()
    connected, summary = connect_phase163_publication_order(bridge)
    manifest = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8-sig"))
    expected = {
        row["reference_id"]: row["publication_position"]
        for row in manifest["assertions"]
    }
    assert summary.manifest_reference_count == 108
    assert summary.manifest_assertion_count == 117
    assert summary.connected_reference_count > 0
    for binding in summary.bindings:
        assert binding.publication_position == expected[binding.reference_id]
        assert connected.registry.reference(binding.reference_id).publication_position == expected[binding.reference_id]


def test_only_exact_reference_ids_are_connected_no_locator_fallback():
    bridge = build_registry_bridge()
    matched_id = next(
        reference_id
        for reference_id in bridge.registry._references
        if reference_id.startswith("toda:")
    )
    original = bridge.registry.reference(matched_id)
    alias_id = "r3b:test:alias:" + matched_id
    bridge.registry.add_reference(LiteratureEntry(
        reference_id=alias_id,
        kind=original.kind,
        locator=original.locator,
        source_id=original.source_id,
    ))

    connected, summary = connect_phase163_publication_order(bridge)
    assert connected.registry.reference(matched_id).publication_position is not None
    assert connected.registry.reference(alias_id) == bridge.registry.reference(alias_id)
    assert connected.registry.reference(alias_id).publication_position is None
    assert alias_id not in {binding.reference_id for binding in summary.bindings}


def test_component_positions_dependencies_and_assertion_objects_are_unchanged():
    bridge = build_registry_bridge()
    connected, _ = connect_phase163_publication_order(bridge)
    assert connected.registry._assertions.keys() == bridge.registry._assertions.keys()
    for assertion_id, original in bridge.registry._assertions.items():
        current = connected.registry.assertion(assertion_id)
        assert current is original
        assert current.component_position == original.component_position
        assert current.dependencies == original.dependencies


def test_records_and_proof_links_are_not_changed():
    bridge = build_registry_bridge()
    connected, summary = connect_phase163_publication_order(bridge)
    assert connected.records is bridge.records
    assert connected.proof_links is bridge.proof_links
    assert summary.proof_link_count == len(bridge.proof_links)


def test_existing_matching_position_is_accepted():
    bridge = build_registry_bridge()
    reference_id = next(
        reference_id
        for reference_id in bridge.registry._references
        if reference_id.startswith("toda:")
    )
    first, _ = connect_phase163_publication_order(bridge)
    expected = first.registry.reference(reference_id).publication_position
    bridge.registry._references[reference_id] = replace(
        bridge.registry.reference(reference_id),
        publication_position=expected,
    )
    second, _ = connect_phase163_publication_order(bridge)
    assert second.registry.reference(reference_id).publication_position == expected


def test_conflicting_existing_position_fails_closed():
    bridge = build_registry_bridge()
    reference_id = next(
        reference_id
        for reference_id in bridge.registry._references
        if reference_id.startswith("toda:")
    )
    first, _ = connect_phase163_publication_order(bridge)
    expected = first.registry.reference(reference_id).publication_position
    bridge.registry._references[reference_id] = replace(
        bridge.registry.reference(reference_id),
        publication_position=expected + 1000,
    )
    with pytest.raises(ValueError, match="conflicts"):
        connect_phase163_publication_order(bridge)


def test_manifest_reference_id_change_does_not_silently_match_by_locator(tmp_path):
    bridge = build_registry_bridge()
    manifest = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8-sig"))
    known_ids = set(bridge.registry._references)
    original_id = next(
        row["reference_id"] for row in manifest["assertions"]
        if row["reference_id"] in known_ids
    )
    original_position = next(
        row["publication_position"] for row in manifest["assertions"]
        if row["reference_id"] == original_id
    )
    for row in manifest["assertions"]:
        if row["reference_id"] == original_id:
            row["reference_id"] = "different:" + original_id
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    connected, summary = connect_phase163_publication_order(bridge, path)
    assert original_position > 0
    assert connected.registry.reference(original_id) == bridge.registry.reference(original_id)
    assert connected.registry.reference(original_id).publication_position is None
    assert original_id not in {binding.reference_id for binding in summary.bindings}
    assert "different:" + original_id not in connected.registry._references
