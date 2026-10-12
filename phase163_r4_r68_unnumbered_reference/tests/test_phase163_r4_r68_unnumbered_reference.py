import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r68_unnumbered_reference import build_proposals, load_inputs, write_reports


@pytest.fixture
def source_data():
    root = Path(__file__).resolve().parents[2]
    return load_inputs(root / "phase163_r4_r66_output" / "boundary_decisions.json", root / "phase163_r4_r67_output" / "context_review.json")


def test_totals_and_read_only(source_data):
    result = build_proposals(*source_data)
    assert result["reference_proposal_count"] == 17
    assert result["assertion_proposal_count"] == 23
    assert result["production_registry_modified"] is False
    assert result["semantic_registration_allowed_count"] == 0


def test_unumbered_conditions_are_statements(source_data):
    result = build_proposals(*source_data)
    candidate = next(r for r in result["records"] if r["editorial_key"] == "extension_coextension_existence_conditions")
    assert candidate["source_numbering_status"] == "UNNUMBERED_PROPOSAL"
    assert (candidate["start_line"], candidate["end_line"]) == (1118, 1121)
    assert [a["assertion_kind_proposal"] for a in candidate["assertions"]] == ["STATEMENT", "STATEMENT"]
    assert [a["component_position_proposal"] for a in candidate["assertions"]] == [1, 2]


def test_original_definitions_stay_distinct(source_data):
    result = build_proposals(*source_data)
    refs = {r["editorial_key"]: r for r in result["records"]}
    for key in ("extension", "coextension"):
        assert refs[key]["assertions"][0]["assertion_kind_proposal"] == "DEFINITION"
    assert refs["nu_n_notation"]["assertions"][1]["component_position_proposal"] == 2
    assert all(r["production_reference_id"] is None for r in result["records"])


def test_context_tampering_rejected(source_data):
    decisions, context = copy.deepcopy(source_data)
    record = next(r for r in context["records"] if r["editorial_key"] == "coextension")
    line = next(l for l in record["surrounding_lines"] if l["line"] == 1119)
    line["text"] = "unrelated"
    with pytest.raises(ValueError, match="differs"):
        build_proposals(decisions, context)


def test_missing_context_line_rejected(source_data):
    decisions, context = copy.deepcopy(source_data)
    record = next(r for r in context["records"] if r["editorial_key"] == "coextension")
    record["surrounding_lines"] = [l for l in record["surrounding_lines"] if l["line"] != 1121]
    with pytest.raises(ValueError, match="Missing existence-condition"):
        build_proposals(decisions, context)


def test_report_written(source_data, tmp_path):
    result = build_proposals(*source_data)
    write_reports(result, tmp_path)
    saved = json.loads((tmp_path / "unnumbered_reference_proposals.json").read_text(encoding="utf-8"))
    assert saved["assertion_proposal_count"] == 23
    assert "番号なし" in (tmp_path / "unnumbered_reference_proposals.md").read_text(encoding="utf-8")
