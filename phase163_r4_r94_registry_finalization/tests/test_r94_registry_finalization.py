"""R94 targeted tests; Phase 163 full suite is intentionally deferred to R95."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from phase163_r4_r93_source_completion.r93_source_completion import classify_gap
from phase163_r4_r94_registry_finalization.r94_registry_finalization import (
    build_ordered_registry,
    finalize_manifest,
    reconcile_bridge,
    write_outputs,
)
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "phase163_r4_r91_output" / "source_catalog.json"
AUDIT_PATH = ROOT / "phase163_r4_r92_output" / "audit.json"
SOURCE_DIR = ROOT / "sources" / "toda"


@pytest.fixture(scope="module")
def evidence():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    completion = classify_gap(catalog, audit, SOURCE_DIR)
    return catalog, audit, completion


@pytest.fixture(scope="module")
def manifest(evidence):
    return finalize_manifest(*evidence)


def test_complete_117_with_stable_ids(evidence, manifest):
    catalog, audit, completion = evidence
    original = {item["source_id"] for item in catalog["records"]}
    original.update(item["source_id"] for item in audit["source_subitems"])
    original.update(item["source_id"] for item in completion["additional_records"])
    final = {item["statement_id"] for item in manifest["assertions"]}
    assert final == original
    assert len(final) == manifest["assertion_count"] == 117
    assert manifest["reference_count"] == 108


def test_publication_order_is_contiguous_and_source_sorted(manifest):
    parents = [r for r in manifest["assertions"] if r["source_origin"] != "R92"]
    assert [r["publication_position"] for r in parents] == list(range(1, 109))
    assert [(r["chapter"], r["start_line"]) for r in parents] == sorted(
        (r["chapter"], r["start_line"]) for r in parents
    )


def test_subitems_share_parent_reference_and_position(manifest):
    rows = {r["statement_id"]: r for r in manifest["assertions"]}
    subitems = [r for r in rows.values() if r["source_origin"] == "R92"]
    assert len(subitems) == 9
    for child in subitems:
        parent = rows[child["parent_statement_id"]]
        assert child["reference_id"] == parent["reference_id"]
        assert child["publication_position"] == parent["publication_position"]
    assert sorted(r["component_position"] for r in subitems if r["locator"] == "Proposition 1.2") == [1, 2, 3, 4, 5]


def test_source_registry_is_detached_and_not_proof_eligible(manifest):
    registry = build_ordered_registry(manifest)
    assert len(registry.assertions_for("toda:Proposition 1.2")) == 6
    for row in manifest["assertions"]:
        entry = registry.assertion(row["statement_id"])
        assert entry.origin is AssertionOrigin.SOURCE_ARCHIVE
        assert entry.content["proof_eligible"] is False
        assert entry.content["mathematics_verified"] is False
        assert entry.available_after_position is None


def test_original_numbers_are_not_automatically_promoted(manifest):
    assert manifest["number_review_count"] == 8
    assert all(item["status"] == "UNVERIFIED_NUMBER_MAPPING_DO_NOT_RENAME" for item in manifest["number_reviews"])
    assert manifest["original_edition_verified"] is False


def test_nested_equation_is_an_alias_not_a_new_reference(manifest):
    alias = manifest["nested_aliases"][0]
    assert alias["parent_locator"] == "Proposition 4.2"
    assert alias["label"] == "4.4"
    assert not any(r["locator"] == "(4.4)" for r in manifest["assertions"])


def test_source_tampering_is_rejected(evidence):
    catalog, audit, completion = evidence
    altered = copy.deepcopy(completion)
    altered["additional_records"][0]["source_text"] += "tampered"
    with pytest.raises(ValueError, match="SHA"):
        finalize_manifest(catalog, audit, altered)


def test_duplicate_statement_id_is_rejected(evidence):
    catalog, audit, completion = evidence
    altered = copy.deepcopy(completion)
    altered["additional_records"][0]["source_id"] = catalog["records"][0]["source_id"]
    with pytest.raises(ValueError, match="identity"):
        finalize_manifest(catalog, audit, altered)


def test_bridge_reconciliation_has_no_proof_links(manifest):
    reconciliation = reconcile_bridge(manifest)
    assert reconciliation["bridge_reference_reused_count"] + reconciliation["bridge_reference_new_count"] == 108
    assert reconciliation["source_only_proof_link_count"] == 0


def test_written_report_and_json_are_complete(manifest, tmp_path):
    reconciliation = {"bridge_reference_reused_count": 20, "bridge_reference_new_count": 88,
                      "bridge_proof_link_count_unchanged": 0, "source_only_proof_link_count": 0}
    write_outputs(manifest, reconciliation, tmp_path)
    reloaded = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert reloaded == manifest
    assert summary["assertion_count"] == 117
    assert "Proposition 1.2" in (tmp_path / "report.md").read_text(encoding="utf-8")
