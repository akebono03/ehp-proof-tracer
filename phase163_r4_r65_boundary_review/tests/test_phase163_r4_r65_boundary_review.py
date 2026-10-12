import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r65_boundary_review import review_packets, write_reports


@pytest.fixture
def inputs():
    root = Path(__file__).resolve().parents[2]
    r64 = json.loads((root / "phase163_r4_r64_output" / "split_proposals.json").read_text(encoding="utf-8"))
    r63 = json.loads((root / "phase163_r4_r63_output" / "source_boundaries.json").read_text(encoding="utf-8"))
    return r64, r63


def test_review_classification_and_no_registration(inputs):
    data = review_packets(*inputs)
    assert data["candidate_count"] == 16
    assert data["assertion_proposal_count"] == 21
    assert data["category_counts"] == {"SOURCE_LOCAL_REVIEW": 9, "CONTEXT_REVIEW": 5, "ADJACENT_NOTATION_REVIEW": 2, "CONTEXT_AND_ADJACENCY_REVIEW": 0}
    assert data["mathematical_boundary_verified_count"] == 0
    assert data["production_registry_modified"] is False


def test_checksum_mismatch_rejected(inputs):
    proposals, boundaries = copy.deepcopy(inputs)
    boundaries["records"][0]["source_span_text"] += "modified"
    with pytest.raises(ValueError, match="checksum mismatch"):
        review_packets(proposals, boundaries)


def test_semantic_approval_rejected(inputs):
    proposals, boundaries = copy.deepcopy(inputs)
    proposals["records"][0]["assertions"][0]["semantic_verification"] = "VERIFIED"
    with pytest.raises(ValueError, match="Unexpected semantic approval"):
        review_packets(proposals, boundaries)


def test_report_written(inputs, tmp_path):
    data = review_packets(*inputs)
    write_reports(data, tmp_path)
    assert json.loads((tmp_path / "review_packets.json").read_text(encoding="utf-8"))["candidate_count"] == 16
    text = (tmp_path / "review_packets.md").read_text(encoding="utf-8")
    assert "外部文脈" in text and "```tex" in text
