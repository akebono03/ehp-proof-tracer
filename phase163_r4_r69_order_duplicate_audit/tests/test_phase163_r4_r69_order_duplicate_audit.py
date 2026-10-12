import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r69_order_duplicate_audit import audit_candidates, load_proposals, write_reports


@pytest.fixture
def source_data():
    root = Path(__file__).resolve().parents[2]
    return load_proposals(root / "phase163_r4_r68_output" / "unnumbered_reference_proposals.json")


def test_counts_and_read_only(source_data):
    result = audit_candidates(source_data)
    assert (result["reference_candidate_count"], result["assertion_candidate_count"]) == (17, 23)
    assert result["unnumbered_reference_candidate_count"] == 1
    assert result["production_registry_modified"] is False
    assert result["production_ids_allocated"] is False


def test_order_and_unverified_publication(source_data):
    records = audit_candidates(source_data)["records"]
    assert [r["candidate_order"] for r in records] == list(range(1, 18))
    assert all(r["publication_position"] is None for r in records)
    assert records[9]["editorial_key"] == "extension_coextension_existence_conditions"
    assert records[9]["component_positions"] == [1, 2]


def test_no_false_duplication_of_adjacent_definitions(source_data):
    result = audit_candidates(source_data)
    assert result["exact_duplicate_evidence_count"] == 0
    assert result["overlapping_source_span_pair_count"] == 0
    pairs = {(r["left"], r["right"]) for r in result["adjacent_source_spans"]}
    assert ("extension_coextension_existence_conditions", "coextension") not in pairs
    assert ("nu_n_notation", "eta_n_cubed_notation") in pairs


def test_reject_duplicate_editorial_key(source_data):
    data = copy.deepcopy(source_data)
    data["records"][1]["editorial_key"] = data["records"][0]["editorial_key"]
    with pytest.raises(ValueError, match="Duplicate editorial keys"):
        audit_candidates(data)


def test_reject_unverified_approval(source_data):
    data = copy.deepcopy(source_data)
    data["records"][0]["publication_position"] = 1
    with pytest.raises(ValueError, match="Unverified publication position"):
        audit_candidates(data)


def test_reject_broken_unnumbered_evidence(source_data):
    data = copy.deepcopy(source_data)
    target = next(r for r in data["records"] if r["editorial_key"] == "extension_coextension_existence_conditions")
    target["source_text"] = "changed"
    with pytest.raises(ValueError, match="checksum mismatch"):
        audit_candidates(data)


def test_write_reports(source_data, tmp_path):
    write_reports(audit_candidates(source_data), tmp_path)
    result = json.loads((tmp_path / "order_duplicate_audit.json").read_text(encoding="utf-8"))
    assert result["assertion_candidate_count"] == 23
    assert len((tmp_path / "order_duplicate_audit.csv").read_text(encoding="utf-8-sig").splitlines()) == 18
    assert "暫定順位" in (tmp_path / "report.md").read_text(encoding="utf-8")
