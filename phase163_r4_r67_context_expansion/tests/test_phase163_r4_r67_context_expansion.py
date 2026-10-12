import copy
import json
import os
from pathlib import Path

import pytest

from phase163_r4_r67_context_expansion import build_context, load_decisions, write_reports


@pytest.fixture
def decisions():
    root = Path(__file__).resolve().parents[2]
    return load_decisions(root / "phase163_r4_r66_output" / "boundary_decisions.json")


@pytest.fixture
def tex_root():
    return Path(os.environ["EHP_R67_TEX_ROOT"])


def test_expected_counts_and_read_only(decisions, tex_root):
    result = build_context(decisions, tex_root)
    assert result["reviewed_reference_count"] == 10
    assert result["reviewed_assertion_count"] == 13
    assert result["mathematical_boundary_verified_count"] == 0
    assert result["production_registry_modified"] is False


def test_source_spans_remain_unchanged(decisions, tex_root):
    result = build_context(decisions, tex_root)
    for record in result["records"]:
        assert record["source_span_sha256_verified"] is True
        original = [x for x in record["surrounding_lines"] if x["region"] == "ORIGINAL"]
        assert len(original) == record["original_end_line"] - record["original_start_line"] + 1


def test_changed_source_is_rejected(decisions, tex_root, tmp_path):
    edited = copy.deepcopy(decisions)
    item = next(x for x in edited["records"] if x["boundary_status"] == "REQUIRES_CONTEXT_OR_SPAN_REVIEW")
    name = item["source_file"]
    original = (tex_root/name).read_text(encoding="utf-8-sig")
    (tmp_path/name).write_text(original.replace(original.splitlines()[item["start_line"]-1], "tampered", 1), encoding="utf-8")
    for other in {x["source_file"] for x in edited["records"] if x["boundary_status"] == "REQUIRES_CONTEXT_OR_SPAN_REVIEW"} - {name}:
        (tmp_path/other).write_bytes((tex_root/other).read_bytes())
    with pytest.raises(ValueError, match="TeX source changed"):
        build_context(edited, tmp_path)


def test_duplicate_identity_rejected(decisions, tmp_path):
    edited = copy.deepcopy(decisions)
    edited["records"][1]["editorial_key"] = edited["records"][0]["editorial_key"]
    path = tmp_path/"decisions.json"
    path.write_text(json.dumps(edited),encoding="utf-8")
    with pytest.raises(ValueError,match="Duplicate editorial keys"):
        load_decisions(path)


def test_report_generation(decisions, tex_root, tmp_path):
    result = build_context(decisions, tex_root)
    write_reports(result,tmp_path)
    assert (tmp_path/"context_review.md").exists()
    assert json.loads((tmp_path/"context_review.json").read_text(encoding="utf-8"))["reviewed_reference_count"] == 10
