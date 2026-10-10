import json
from pathlib import Path

import pytest

from phase163_r4_r36_page7_review.review import (
    EVIDENCE, EXPECTED_SHA256, REQUIRED, review_page_seven, run, sha256, validate_inputs,
)

HERE = Path(__file__).resolve().parents[1]

def baseline():
    return (HERE / "R35_BASELINE.tex").read_text(encoding="utf-8")

def ledger():
    return json.loads((HERE / "R35_PAGE_LEDGER.json").read_text(encoding="utf-8"))

def test_expected_source_hash():
    assert sha256(baseline()) == EXPECTED_SHA256

def test_page7_anchors_exist():
    assert all(fragment in baseline() for fragment in REQUIRED)

def test_expected_input_acceptance():
    validate_inputs(baseline(), ledger())

def test_unexpected_input_rejected():
    with pytest.raises(ValueError, match="SHA-256"):
        validate_inputs(baseline() + "x", ledger())

def test_wrong_page_ledger_rejected():
    wrong = ledger()
    wrong[2]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="statuses"):
        review_page_seven(baseline(), wrong)

def test_invalid_ledger_length_rejected():
    with pytest.raises(ValueError, match="eleven"):
        validate_inputs(baseline(), ledger()[:-1])

def test_preserve_previous_pages_and_unverified_page7():
    reviewed = review_page_seven(baseline(), ledger())
    assert [p["status"] for p in reviewed] == ["VERIFIED"] * 2 + ["UNVERIFIED"] * 9
    assert reviewed[:2] == ledger()[:2]
    assert reviewed[3:] == ledger()[3:]
    assert reviewed[2]["unresolved_original_discrepancies"][0]["auto_corrected"] is False

def test_evidence_includes_source_conflict():
    assert len(EVIDENCE) == 9
    assert any(row[3] == "ORIGINAL_MATH_CONFLICT" for row in EVIDENCE)

def test_run_outputs_utf8_without_tex_changes(tmp_path):
    src = tmp_path / "input.tex"
    src.write_text(baseline(), encoding="utf-8")
    led = tmp_path / "ledger.json"
    led.write_text(json.dumps(ledger(), ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "output"
    result = run(src, led, output)
    assert result["new_confirmed_corrections"] == 0
    assert result["status_counts"] == {"VERIFIED": 2, "UNVERIFIED": 9, "CORRECTION_REQUIRED": 0}
    assert (output / "Toda_01_corrected.tex").read_text(encoding="utf-8") == baseline()
    assert (output / "page7_evidence.csv").exists()
    assert (output / "report.md").exists()
