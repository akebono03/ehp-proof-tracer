import copy
import csv
import json
from pathlib import Path

import pytest

from phase163_r4_r70_pending_batch_audit import audit_pending, lexical_bucket, write_reports


@pytest.fixture
def inputs():
    root = Path(__file__).resolve().parents[2]
    r51 = json.loads((root / "phase163_r4_r51_output" / "review.json").read_text(encoding="utf-8-sig"))
    r69 = json.loads((root / "phase163_r4_r69_output" / "order_duplicate_audit.json").read_text(encoding="utf-8-sig"))
    return r51, r69


def test_full_pending_inventory(inputs):
    result = audit_pending(*inputs)
    assert result["pending_candidate_count"] == 237
    assert len(result["records"]) == 237
    assert sum(result["lexical_bucket_counts"].values()) == 237
    assert sum(result["chapter_counts"].values()) == 237
    assert len({r["r48_index"] for r in result["records"]}) == 237


def test_only_pending_roles(inputs):
    r51, r69 = inputs
    result = audit_pending(r51, r69)
    pending_ids = {r["r48_index"] for r in r51["review_queue"] if r["role_decision"] == "PENDING_MATHEMATICAL_REVIEW"}
    assert {r["r48_index"] for r in result["records"]} == pending_ids


def test_no_semantic_approval_or_ids(inputs):
    result = audit_pending(*inputs)
    assert result["mathematical_role_verified_count"] == 0
    assert result["semantic_duplicate_verified_count"] == 0
    assert result["production_registry_modified"] is False
    assert all(r["registration_action"] == "NONE" and r["production_reference_id"] is None for r in result["records"])


def test_lexical_bucket_not_semantic():
    assert lexical_bucket(r"\nu_n:=E^n\nu_4") == "DEFINITION_SYNTAX_REVIEW"
    assert lexical_bucket(r"f\rightarrow g") == "MAP_SYNTAX_REVIEW"
    assert lexical_bucket(r"a=b") == "RELATION_SYNTAX_REVIEW"
    assert lexical_bucket("x") == "OTHER_DISPLAY_REVIEW"


def test_cardinality_corruption_rejected(inputs):
    r51, r69 = copy.deepcopy(inputs)
    r51["pending_mathematical_review_count"] = 238
    with pytest.raises(ValueError, match="pending count"):
        audit_pending(r51, r69)


def test_duplicate_index_rejected(inputs):
    r51, r69 = copy.deepcopy(inputs)
    r51["review_queue"][1]["r48_index"] = 1
    with pytest.raises(ValueError, match="duplicated or missing"):
        audit_pending(r51, r69)


def test_registered_pending_rejected(inputs):
    r51, r69 = copy.deepcopy(inputs)
    target = next(x for x in r51["review_queue"] if x["role_decision"] == "PENDING_MATHEMATICAL_REVIEW")
    target["registration_decision"] = "APPLIED"
    with pytest.raises(ValueError, match="already classified or registered"):
        audit_pending(r51, r69)


def test_reports(inputs, tmp_path):
    result = audit_pending(*inputs)
    write_reports(result, tmp_path)
    assert len(json.loads((tmp_path / "pending_batch_audit.json").read_text(encoding="utf-8"))["records"]) == 237
    with (tmp_path / "pending_batch_audit.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        csv_rows = list(csv.DictReader(stream))
    assert len(csv_rows) == 237
    assert {int(row["r48_index"]) for row in csv_rows} == {row["r48_index"] for row in result["records"]}
    excerpts = {row["r48_index"]: row["excerpt"] for row in result["records"]}
    assert all(row["excerpt"] == excerpts[int(row["r48_index"])] for row in csv_rows)
    assert "237" in (tmp_path / "report.md").read_text(encoding="utf-8")
