from pathlib import Path

import pytest

from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r85_archive_bridge import build_registry_bridge_with_source_archive
from phase163_source_archive_registry import CATALOG_PATH, build_registry_with_source_archive
from unified_statement_registry import AssertionOrigin


def test_opt_in_bridge_keeps_archival_entries_separate():
    bridge = build_registry_bridge_with_source_archive()
    archival = bridge.records_for("source_archive")
    assert len(archival) == 8
    assert all(row.status is MigrationStatus.METADATA_ONLY for row in archival)
    assert all(bridge.registry.assertion(row.assertion_id).origin is AssertionOrigin.SOURCE_ARCHIVE for row in archival)


def test_base_bridge_unchanged_by_opt_in():
    before = build_registry_bridge()
    combined = build_registry_bridge_with_source_archive()
    after = build_registry_bridge()
    assert before.records == after.records
    assert before.proof_links == after.proof_links
    assert not before.records_for("source_archive")
    assert len(combined.records) == len(before.records) + 8


def test_proof_links_are_preserved_without_new_archival_links():
    original = build_registry_bridge()
    combined = build_registry_bridge_with_source_archive()
    assert combined.proof_links == original.proof_links
    archive_ids = {row.assertion_id for row in combined.records_for("source_archive")}
    assert all(link.assertion_id not in archive_ids for link in combined.proof_links)


def test_archive_is_not_eligible_for_proof():
    combined = build_registry_bridge_with_source_archive()
    for row in combined.records_for("source_archive"):
        item = combined.registry.assertion(row.assertion_id)
        assert item.available_after_position is None
        assert item.content["proof_eligible"] is False
        assert item.content["mathematics_verified"] is False


def test_existing_proposition_reference_reused():
    combined = build_registry_bridge_with_source_archive()
    assert len(combined.registry.assertions_for("toda:Proposition 2.5")) >= 3
    assert sum(x.assertion_id.startswith("archive:") for x in combined.registry.assertions_for("toda:Proposition 2.5")) == 2


def test_builder_injects_only_one_existing_bridge(monkeypatch):
    import phase163_source_archive_registry as archive
    bridge = build_registry_bridge()
    def should_not_build_again():
        raise AssertionError("created second Bridge")
    monkeypatch.setattr(archive, "build_registry_bridge", should_not_build_again)
    registry, summary = build_registry_with_source_archive(bridge=bridge)
    assert registry is bridge.registry
    assert summary["source_text_assertion_added_count"] == 8


def test_archive_checksum_failure_blocks_integration(tmp_path):
    import json
    data = __import__("phase163_source_archive_registry").load_source_archive_catalog()
    data["records"][0]["claim_text"] += "tampered"
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        build_registry_bridge_with_source_archive(path)


def test_repeatable_independent_bridges():
    first = build_registry_bridge_with_source_archive()
    second = build_registry_bridge_with_source_archive()
    assert first.registry is not second.registry
    assert first.records_for("source_archive") == second.records_for("source_archive")
