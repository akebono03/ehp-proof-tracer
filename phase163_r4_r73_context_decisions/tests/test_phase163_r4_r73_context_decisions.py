import csv
import importlib.util
import json
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "phase163_r4_r73_context_decisions.py"
SPEC = importlib.util.spec_from_file_location("r73", MODULE)
r73 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(r73)


@pytest.fixture
def source():
    path = Path.cwd() / "phase163_r4_r72_output" / "role_proposals.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_complete_preservation(source):
    result = r73.build_review(source)
    assert len(result["records"]) == 237
    assert {row["r48_index"] for row in result["records"]} == {row["r48_index"] for row in source["records"]}


def test_explicit_decisions_only(source):
    result = r73.build_review(source)
    new = [row for row in result["records"] if row["r73_individually_reviewed"]]
    assert len(new) == len(r73.DECISIONS)
    assert all(row["r48_index"] in r73.DECISIONS for row in new)


def test_previous_reviews_unchanged(source):
    result = r73.build_review(source)
    for before, after in zip(source["records"], result["records"]):
        if before["proposed_role"] != "UNREVIEWED":
            assert after["proposed_role"] == before["proposed_role"]
            assert after["proposal_rationale"] == before["proposal_rationale"]


def test_no_approval_or_mutation(source):
    result = r73.build_review(source)
    assert result["mathematical_role_verified_count"] == 0
    assert result["semantic_registration_allowed_count"] == 0
    assert result["production_registry_modified"] is False
    assert result["production_ids_allocated"] is False
    assert result["full_suite_run"] is False


def test_rejects_wrong_phase(source):
    source["phase"] = "163 R4-R71"
    with pytest.raises(ValueError, match="contract"):
        r73.build_review(source)


def test_rejects_modified_excerpt(source):
    index = next(iter(r73.DECISIONS))
    row = next(row for row in source["records"] if row["r48_index"] == index)
    row["excerpt"] += "changed"
    with pytest.raises(ValueError, match="hash mismatch"):
        r73.build_review(source)


def test_rejects_duplicate_record(source):
    source["records"][0]["r48_index"] = source["records"][1]["r48_index"]
    with pytest.raises(ValueError, match="unique"):
        r73.build_review(source)


def test_csv_counts_multiline_tex(source, tmp_path):
    result = r73.build_review(source)
    r73.write_reports(result, tmp_path)
    with (tmp_path / "role_decisions.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 237
    assert rows[0]["excerpt"] == result["records"][0]["excerpt"]
    assert json.loads((tmp_path / "role_decisions.json").read_text(encoding="utf-8")) == result


def test_deterministic(source):
    assert r73.build_review(source) == r73.build_review(source)
