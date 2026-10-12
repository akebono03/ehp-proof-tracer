import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r87_semantic_gate import build_gate, write_outputs


DATA = Path(__file__).resolve().parents[1] / "claim_review_catalog.json"


def input_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_nine_review_units_and_no_eligibility():
    result = build_gate(input_data())
    assert result["review_unit_count"] == 9
    assert result["semantic_registration_allowed_count"] == 0
    assert result["proof_eligible_count"] == 0
    assert all(not row["mathematical_semantics_verified"] for row in result["records"])


def test_even_dimension_is_split():
    result = build_gate(input_data())
    parts = [r for r in result["records"] if r["source_owner"] == "thm:2.4"]
    assert [(r["component_position"], r["subposition"]) for r in parts] == [(1, 1), (2, 1), (2, 2)]
    assert "p-成分に限定" in parts[-1]["required_scope_conditions_jp"]


def test_proposition_25_preserves_equalities():
    result = build_gate(input_data())
    rows = [r for r in result["records"] if r["source_owner"] == "prop:2.5"]
    assert len(rows) == 2
    assert all(any("j<3m-1" in c for c in x["required_scope_conditions_jp"]) for x in rows)


def test_source_text_tampering_rejected():
    data = input_data()
    data["records"][0]["claim_text"] += " altered"
    with pytest.raises(ValueError, match="tampered"):
        build_gate(data)


def test_missing_review_unit_rejected():
    data = input_data()
    data["records"].pop()
    with pytest.raises(ValueError):
        build_gate(data)


def test_review_duplicate_rejected():
    data = input_data()
    data["records"][1]["review_unit_id"] = data["records"][0]["review_unit_id"]
    with pytest.raises(ValueError):
        build_gate(data)


def test_unverified_boundary_enforced():
    data = input_data()
    data["records"][0]["proof_eligible"] = True
    with pytest.raises(ValueError, match="non-certified"):
        build_gate(data)


def test_alias_label_enforced():
    data = input_data()
    row = next(r for r in data["records"] if r["source_owner"] == "prop:4.2")
    row["claim_text"] = row["claim_text"].replace("label{4.4}", "label{4.5}")
    import hashlib
    row["claim_sha256"] = hashlib.sha256(row["claim_text"].encode()).hexdigest()
    with pytest.raises(ValueError, match="alias"):
        build_gate(data)


def test_output(tmp_path):
    result = build_gate(input_data())
    write_outputs(result, tmp_path)
    assert json.loads((tmp_path / "semantic_registration_gate.json").read_text(encoding="utf-8"))["review_unit_count"] == 9
    assert "正式登録" in (tmp_path / "report.md").read_text(encoding="utf-8")
