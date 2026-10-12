import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r90_bridge_nine.phase163_r4_r90_bridge_nine import (
    DEFAULT_R86,
    DEFAULT_R88,
    build_registry_bridge_with_r89_nine,
    write_report,
)
from unified_statement_registry import AssertionOrigin, ReferenceKind


@dataclass(frozen=True)
class Component:
    reference_locator: str
    component_key: str
    order: int = 1
    range_text: str | None = None


def empty_bridge():
    return build_registry_bridge(components_by_reference={}, theorem_facts=SimpleNamespace(entries=()))


def test_nine_source_assertions_into_existing_bridge():
    base = build_registry_bridge(
        components_by_reference={"Proposition 2.5": (
            Component("Proposition 2.5", "existing_component"),
        )},
        theorem_facts=SimpleNamespace(entries=()),
    )
    combined, report = build_registry_bridge_with_r89_nine(base=base)
    assert combined.registry is base.registry
    assert report["reference_added_count"] == 3
    assert report["reference_reused_count"] == 1
    assert report["assertion_added_count"] == 9
    assert len(combined.records_for("r89_source_archive")) == 9
    assert all(row.status is MigrationStatus.METADATA_ONLY
               for row in combined.records_for("r89_source_archive"))
    assert combined.registry.assertions_for("toda:Proposition 2.5")[0].assertion_id.startswith("boundary:")
    assert len(combined.registry.assertions_for("toda:Proposition 2.5")) == 3


def test_mathematical_certification_and_proof_links_remain_absent():
    base = empty_bridge()
    before = base.proof_links
    combined, report = build_registry_bridge_with_r89_nine(base=base)
    assert combined.proof_links == before
    assert report["proof_eligible_count"] == 0
    assert report["proof_search_connected"] is False
    for row in combined.records_for("r89_source_archive"):
        item = combined.registry.assertion(row.assertion_id)
        assert item.origin is AssertionOrigin.SOURCE_ARCHIVE
        assert item.content["proof_eligible"] is False
        assert item.content["mathematics_verified"] is False
        assert item.available_after_position is None


def test_same_reference_two_subpositions():
    combined, report = build_registry_bridge_with_r89_nine(base=empty_bridge())
    entries = combined.registry.assertions_for("toda:Theorem 2.4")
    assert [(x.component_position, x.content["subposition"]) for x in entries] == [
        (1, 1), (2, 1), (2, 2),
    ]
    assert report["assertion_added_count"] == 9


def test_reference_identity_conflict_rejected_without_insertions():
    base = build_registry_bridge(
        components_by_reference={"Proposition 2.5": (Component("Proposition 2.5", "x"),)},
        theorem_facts=SimpleNamespace(entries=()),
    )
    base.registry._references["toda:Proposition 2.5"] = __import__("unified_statement_registry").LiteratureEntry(
        "toda:Proposition 2.5", ReferenceKind.LEMMA, "Proposition 2.5"
    )
    with pytest.raises(ValueError, match="reference conflict"):
        build_registry_bridge_with_r89_nine(base=base)
    assert len(base.registry.assertions_for("toda:Proposition 2.5")) == 1


def test_duplicate_archive_ids_rejected():
    base = empty_bridge()
    build_registry_bridge_with_r89_nine(base=base)
    with pytest.raises(ValueError, match="duplicate source assertion IDs"):
        build_registry_bridge_with_r89_nine(base=base)


def test_corrupted_R89_input_rejected(tmp_path):
    r86 = json.loads(DEFAULT_R86.read_text(encoding="utf-8"))
    r86["records"][0]["claim_text"] += "modified"
    bad = tmp_path / "tampered.json"
    bad.write_text(json.dumps(r86, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="digest"):
        build_registry_bridge_with_r89_nine(r86_path=bad, base=empty_bridge())


def test_independent_builds_and_original_bridge_not_modified():
    before = build_registry_bridge()
    first, one = build_registry_bridge_with_r89_nine()
    second, two = build_registry_bridge_with_r89_nine()
    after = build_registry_bridge()
    assert one == two
    assert first.registry is not second.registry
    assert before.records == after.records
    assert before.proof_links == after.proof_links
    assert len(first.records) == len(before.records) + 9
    assert first.proof_links == before.proof_links


def test_report_written(tmp_path):
    _, report = build_registry_bridge_with_r89_nine(base=empty_bridge())
    write_report(report, tmp_path)
    saved = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert saved["assertion_added_count"] == 9
    assert "数学的認定" in (tmp_path / "report.md").read_text(encoding="utf-8")
