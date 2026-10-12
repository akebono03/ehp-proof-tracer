import json
from pathlib import Path

import pytest

from phase163_source_archive_registry import (
    CATALOG_PATH,
    build_registry_with_source_archive,
    load_source_archive_catalog,
)


def test_archive_catalog_eight_entries_and_scope():
    source = load_source_archive_catalog()
    assert len(source["records"]) == 8
    assert all(row["shared_scope_note"] for row in source["records"])


def test_register_into_real_live_bridge():
    registry, result = build_registry_with_source_archive()
    assert result["reference_added_count"] == 3
    assert result["reference_reused_count"] == 1
    assert result["source_text_assertion_added_count"] == 8
    assert len(registry.assertions_for("toda:Proposition 2.5")) >= 3


def test_existing_boundary_is_preserved():
    registry, result = build_registry_with_source_archive()
    source_entries = registry.assertions_for("toda:Proposition 2.5")
    assert any(entry.assertion_id.startswith("boundary:") for entry in source_entries)
    assert sum(entry.assertion_id.startswith("archive:") for entry in source_entries) == 2


def test_proof_ineligible_all_entries():
    registry, result = build_registry_with_source_archive()
    assert result["proof_eligible_count"] == 0
    for identity in result["source_text_assertion_ids"]:
        assertion = registry.assertion(identity)
        assert assertion.content["proof_eligible"] is False
        assert assertion.content["mathematics_verified"] is False
        assert assertion.available_after_position is None


def test_same_call_is_reproducible_without_mutating_global_bridge():
    first, summary1 = build_registry_with_source_archive()
    second, summary2 = build_registry_with_source_archive()
    assert summary1 == summary2
    assert first is not second
    assert len(first.assertions_for("toda:Proposition 1.6")) == 3


def test_tampering_is_detected(tmp_path):
    item = load_source_archive_catalog()
    item["records"][0]["claim_text"] += "tampered"
    altered = tmp_path / "altered.json"
    altered.write_text(json.dumps(item, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        load_source_archive_catalog(altered)


def test_duplicate_component_is_rejected(tmp_path):
    item = load_source_archive_catalog()
    item["records"][1]["proposed_assertion_key"] = item["records"][0]["proposed_assertion_key"]
    altered = tmp_path / "duplicate.json"
    altered.write_text(json.dumps(item, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError):
        load_source_archive_catalog(altered)


def test_order_change_is_rejected(tmp_path):
    item = load_source_archive_catalog()
    item["records"][0]["component_position"] = 2
    altered = tmp_path / "position.json"
    altered.write_text(json.dumps(item, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="order"):
        load_source_archive_catalog(altered)
