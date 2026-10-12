import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r66_multi_assertion_boundary import build_review, write_reports


@pytest.fixture
def r65_data():
    root = Path(__file__).resolve().parents[2]
    return json.loads((root / "phase163_r4_r65_output" / "review_packets.json").read_text(encoding="utf-8"))


def test_one_reference_many_assertions(r65_data):
    result = build_review(r65_data)
    assert result["reference_proposal_count"] == 16
    assert result["assertion_proposal_count"] == 21
    assert result["multi_assertion_reference_count"] == 5
    assert all(item["reference_count_proposed"] == 1 for item in result["records"])


def test_review_flags_and_safe_boundary(r65_data):
    result = build_review(r65_data)
    by_key = {r["editorial_key"]: r for r in result["records"]}
    assert "TRAILING_SENTENCE_OUTSIDE_SPAN" in by_key["pointed_homotopy_classes"]["review_flags"]
    assert "DEFINITION_HYPOTHESES_AND_INDETERMINACY" in by_key["stable_toda_bracket"]["review_flags"]
    assert result["mathematical_boundary_verified_count"] == 0
    assert result["semantic_registration_allowed_count"] == 0
    assert result["production_ids_allocated"] is False


def test_missing_marker_is_rejected(r65_data):
    broken = copy.deepcopy(r65_data)
    broken["records"][0]["source_span_text"] = "removed"
    with pytest.raises(ValueError, match="Missing evidence"):
        build_review(broken)


def test_malformed_component_order_is_rejected(r65_data):
    broken = copy.deepcopy(r65_data)
    target = next(r for r in broken["records"] if r["editorial_key"] == "nu_n_notation")
    target["assertions"][1]["component_position_proposal"] = 1
    with pytest.raises(ValueError, match="Invalid component order"):
        build_review(broken)


def test_semantic_approval_is_rejected(r65_data):
    broken = copy.deepcopy(r65_data)
    broken["semantic_registration_allowed_count"] = 1
    with pytest.raises(ValueError, match="Unexpected semantic approval"):
        build_review(broken)


def test_reports_written(r65_data, tmp_path):
    report = build_review(r65_data)
    write_reports(report, tmp_path)
    assert json.loads((tmp_path / "boundary_decisions.json").read_text(encoding="utf-8"))["reference_proposal_count"] == 16
    assert "pointed_homotopy_classes" in (tmp_path / "boundary_decisions.md").read_text(encoding="utf-8")
