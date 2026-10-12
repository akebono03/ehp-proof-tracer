"""R93 targeted tests; full suite is not run here."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from phase163_r4_r93_source_completion.r93_source_completion import (
    classify_gap,
    digest,
    register_completion,
    write_outputs,
)
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "phase163_r4_r91_output" / "source_catalog.json"
R92_AUDIT = ROOT / "phase163_r4_r92_output" / "audit.json"
SOURCE = ROOT / "sources" / "toda"


def load_data():
    return (json.loads(CATALOG.read_text(encoding="utf-8")),
            json.loads(R92_AUDIT.read_text(encoding="utf-8")))


def test_r92_gap_count_is_fourteen():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    assert result["gap_candidate_count"] == 14
    assert len(result["additional_records"]) == 12
    assert len(result["nested_aliases"]) == 1
    assert len(result["duplicate_mentions"]) == 1


def test_chapter_one_eleven_equations_and_definition():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    equations = [r for r in result["additional_records"] if r["kind"] == "equation"]
    definitions = [r for r in result["additional_records"] if r["kind"] == "definition"]
    assert len(equations) == 11
    assert len(definitions) == 1
    assert all(r["chapter"] == 1 and r["review_needed"] for r in equations)
    assert "secondary composition" in definitions[0]["source_text"]


def test_nested_4_4_not_double_registered():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    nested = result["nested_aliases"][0]
    assert nested["parent_locator"] == "Proposition 4.2"
    assert nested["label"] == "4.4"
    assert all(r["chapter"] != 4 for r in result["additional_records"])


def test_chapter_two_is_mention_not_new_definition():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    assert result["duplicate_mentions"][0]["chapter"] == 2
    assert all(r["chapter"] != 2 for r in result["additional_records"])


def test_r91_and_r92_evidence_rechecked():
    catalog, audit = load_data()
    changed = copy.deepcopy(audit)
    changed["gap_candidates"][0]["line"] += 1
    with pytest.raises(ValueError, match="R92 audit differs"):
        classify_gap(catalog, changed, SOURCE)


def test_r93_source_sha_and_unique_ids():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    entries = result["additional_records"]
    assert len({r["source_id"] for r in entries}) == 12
    assert all(digest(r["source_text"]) == r["source_sha256"] for r in entries)


def test_number_mapping_maintained_as_review_only():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    assert len(result["number_reviews"]) == 8
    assert all(row["status"] == "UNVERIFIED_NUMBER_MAPPING_DO_NOT_RENAME" for row in result["number_reviews"])


def test_registry_contains_all_117_source_assertions():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    registry, summary = register_completion(catalog, audit, result)
    assert summary["source_only_assertion_count"] == 117
    ids = ([r["source_id"] for r in catalog["records"]]
           + [r["source_id"] for r in audit["source_subitems"]]
           + [r["source_id"] for r in result["additional_records"]])
    assert len(set(ids)) == 117
    for identifier in ids:
        assertion = registry.assertion(identifier)
        assert assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        assert assertion.available_after_position is None
        assert assertion.content["proof_eligible"] is False
    assert summary["production_registry_modified"] is False
    assert summary["proof_search_connected"] is False


def test_changed_source_sha_blocks_registration():
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    bad = copy.deepcopy(result)
    bad["additional_records"][0]["source_text"] += "malicious edit"
    with pytest.raises(ValueError, match="tampering"):
        register_completion(catalog, audit, bad)


def test_report_written(tmp_path):
    catalog, audit = load_data()
    result = classify_gap(catalog, audit, SOURCE)
    _, summary = register_completion(catalog, audit, result)
    write_outputs(result, summary, tmp_path)
    assert (tmp_path / "completion.json").exists()
    assert (tmp_path / "registration.json").exists()
    assert "117件" in (tmp_path / "report.md").read_text(encoding="utf-8")
