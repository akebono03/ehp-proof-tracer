import copy
import csv
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "phase163_r4_r71_semantic_review_queue.py"
spec = importlib.util.spec_from_file_location("r71", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.fixture
def source():
    root = Path(__file__).resolve().parents[2]
    return module.load_input(root / "phase163_r4_r70_output" / "pending_batch_audit.json")


def test_all_candidates_accounted(source):
    report = module.audit_queue(source)
    assert len(report["records"]) == 237
    assert sum(report["review_tier_counts"].values()) == 237
    assert len({r["r48_index"] for r in report["records"]}) == 237


def test_two_overlaps_three_nearby(source):
    report = module.audit_queue(source)
    assert report["overlap_review_count"] == 2
    assert report["nearby_review_count"] == 3
    assert report["review_tier_counts"]["T0_EXISTING_REFERENCE_SPAN"] == 2
    assert report["review_tier_counts"]["T1_ADJACENT_REFERENCE"] == 3


def test_no_semantic_certification_or_mutation(source):
    report = module.audit_queue(source)
    assert report["mathematical_role_verified_count"] == 0
    assert report["registration_allowed_count"] == 0
    assert report["production_registry_modified"] is False
    assert all(r["review_decision"] == "NEEDS_MATHEMATICAL_REVIEW" for r in report["records"])


def test_bad_excerpt_digest_fails(source):
    changed = copy.deepcopy(source)
    changed["records"][0]["excerpt"] += "x"
    with pytest.raises(ValueError, match="hash mismatch"):
        module.audit_queue(changed)


def test_duplicate_identity_fails(source):
    changed = copy.deepcopy(source)
    changed["records"][1]["r48_index"] = changed["records"][0]["r48_index"]
    with pytest.raises(ValueError, match="identity"):
        module.audit_queue(changed)


def test_wrong_source_phase_fails(source):
    changed = copy.deepcopy(source)
    changed["phase"] = "untrusted"
    with pytest.raises(ValueError, match="R70"):
        module.audit_queue(changed)


def test_full_multiline_csv_records(source, tmp_path):
    result = module.audit_queue(source)
    module.write_reports(result, tmp_path)
    with (tmp_path / "semantic_review_queue.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 237
    assert any("\n" in row["excerpt"] for row in rows)
    assert len(json.loads((tmp_path / "semantic_review_queue.json").read_text(encoding="utf-8"))["records"]) == 237
    assert "237候補" in (tmp_path / "report.md").read_text(encoding="utf-8")


def test_repeatable(source):
    assert module.audit_queue(source) == module.audit_queue(source)
