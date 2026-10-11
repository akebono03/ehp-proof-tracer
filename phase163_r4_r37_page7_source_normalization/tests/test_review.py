import json
from pathlib import Path

import pytest

from phase163_r4_r37_page7_source_normalization.review import (
    EXPECTED_SHA256, NORMALIZED_FORMULA, ORIGINAL_FORMULA,
    reconcile, run, sha256, source_record, validate,
)

HERE = Path(__file__).resolve().parents[1]


def baseline():
    return (HERE / "R36_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((HERE / "R36_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_source_sha256():
    assert sha256(baseline()) == EXPECTED_SHA256


def test_source_and_normalization_remain_distinct():
    record = source_record()
    assert record["source_formula_tex"] == ORIGINAL_FORMULA
    assert record["editorial_normalization_tex"] == NORMALIZED_FORMULA
    assert ORIGINAL_FORMULA != NORMALIZED_FORMULA


def test_original_typo_not_claimed():
    record = source_record()
    assert record["source_typo_status"] == "POSSIBLE_NOT_ESTABLISHED"
    assert record["proof_search_eligible"] is False


def test_bad_tex_rejected():
    with pytest.raises(ValueError, match="SHA-256"):
        validate(baseline() + "modified", ledger())


def test_bad_ledger_rejected():
    l = ledger()
    l[2]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="page status"):
        validate(baseline(), l)


def test_missing_prior_discrepancy_rejected():
    l = ledger()
    l[2]["unresolved_original_discrepancies"] = []
    with pytest.raises(ValueError, match="evidence missing"):
        validate(baseline(), l)


def test_statuses_preserved_and_no_auto_correction():
    updated, record = reconcile(baseline(), ledger())
    assert [r["status"] for r in updated] == ["VERIFIED"] * 2 + ["UNVERIFIED"] * 9
    assert updated[0:2] == ledger()[0:2]
    assert updated[3:] == ledger()[3:]
    assert updated[2]["unresolved_original_discrepancies"][0]["auto_corrected"] is False
    assert record["editorial_tex_modified"] is False


def test_run_writes_utf8_full_source(tmp_path):
    input_tex = tmp_path / "input.tex"
    input_tex.write_text(baseline(), encoding="utf-8")
    input_ledger = tmp_path / "ledger.json"
    input_ledger.write_text(json.dumps(ledger(), ensure_ascii=False), encoding="utf-8")
    summary = run(input_tex, input_ledger, tmp_path / "out")
    assert summary["new_confirmed_corrections"] == 0
    assert (tmp_path / "out" / "Toda_01_corrected.tex").read_text(encoding="utf-8") == baseline()
    assert (tmp_path / "out" / "source_normalization.json").exists()
    assert summary["status_counts"]["VERIFIED"] == 2
    assert summary["status_counts"]["UNVERIFIED"] == 9
