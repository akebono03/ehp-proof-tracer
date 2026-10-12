import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r88_claim_conditions import assess, tail_key, write_outputs


ROOT = Path(__file__).resolve().parents[1]


def sources():
    return (
        json.loads((ROOT / "r86_claim_review_snapshot.json").read_text(encoding="utf-8")),
        json.loads((ROOT / "r87_semantic_gate_snapshot.json").read_text(encoding="utf-8")),
    )


def test_all_nine_claims_and_no_promotion():
    result = assess(*sources())
    assert result["source_scope_token_verified_count"] == 9
    assert result["mathematical_semantics_verified_count"] == 0
    assert result["production_registry_modified"] is False


def test_first_argument_case_removes_prior_sentence():
    r86, r87 = sources()
    row = next(x for x in r86["records"] if tail_key(x["review_unit_id"]) == "prop:1-6:first_argument_additivity")
    assert row["claim_text"].startswith("$n\\ge 1$")
    assert assess(r86, r87)["review_unit_count"] == 9


def test_proposition25_equality_is_inherited():
    result = assess(*sources())
    rows = [x for x in result["records"] if x["reference_locator"] == "Proposition 2.5"]
    assert len(rows) == 2
    assert all("BOTH_FORMULAS_INHERIT_EQUALITY_CASES" in x["verified_source_checks"] for x in rows)


def test_even_dimensional_claims_have_same_position_and_distinct_subpositions():
    result = assess(*sources())
    rows = [x for x in result["records"] if x["reference_locator"] == "Theorem 2.4"]
    assert [(x["component_position"], x["subposition"]) for x in rows] == [(1, 1), (2, 1), (2, 2)]


def test_tampered_claim_rejected():
    r86, r87 = sources()
    r86["records"][0]["claim_text"] += "BAD"
    with pytest.raises(AssertionError, match="checksum"):
        assess(r86, r87)


def test_tampered_condition_rejected_even_with_recomputed_digest():
    import hashlib
    r86, r87 = sources()
    r86["records"][0]["claim_text"] = r86["records"][0]["claim_text"].replace("W=\\Ex W'", "W=X")
    r86["records"][0]["claim_sha256"] = hashlib.sha256(r86["records"][0]["claim_text"].encode("utf-8")).hexdigest()
    r87["records"][0]["claim_sha256"] = r86["records"][0]["claim_sha256"]
    with pytest.raises(AssertionError, match="condition not found"):
        assess(r86, r87)


def test_unexpected_promotion_rejected():
    r86, r87 = sources()
    r87["records"][0]["proof_eligible"] = True
    with pytest.raises(AssertionError, match="approval"):
        assess(r86, r87)


def test_missing_common_equality_rejected():
    r86, r87 = sources()
    for row in r86["records"]:
        if row["reference_locator"] == "Proposition 2.5":
            row["inherited_equality_conditions"] = None
    with pytest.raises(AssertionError, match="shared equality"):
        assess(r86, r87)


def test_json_and_report_written(tmp_path):
    result = assess(*sources())
    write_outputs(result, tmp_path)
    assert json.loads((tmp_path / "scope_conditions.json").read_text(encoding="utf-8"))["review_unit_count"] == 9
    assert "正式 ID" in (tmp_path / "report.md").read_text(encoding="utf-8")
