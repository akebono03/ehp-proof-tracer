import json
from pathlib import Path

import pytest

from phase163_r4_r31_page5_verification.verify import (
    EXPECTED_SHA256,
    REVIEW_FIELDS,
    run,
    sha256,
    validate_inputs,
    verify_page_five,
)


PACKAGE = Path(__file__).resolve().parents[1]


def baseline():
    return (PACKAGE / "R30_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((PACKAGE / "R30_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_digest():
    assert sha256(baseline()) == EXPECTED_SHA256


def test_ledger_and_source_are_compatible():
    validate_inputs(baseline(), ledger())


def test_reject_unexpected_tex():
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        validate_inputs(baseline() + "changed", ledger())


def test_reject_tampered_ledger():
    entries = ledger()
    entries[1]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="Unexpected prior"):
        validate_inputs(baseline(), entries)


def test_page_five_semantic_verified_all_five_facets():
    rows = verify_page_five(ledger())
    assert rows[0]["status"] == "VERIFIED"
    assert all(rows[0]["review"][field] for field in REVIEW_FIELDS)
    assert rows[0]["verbatim_transcription_verified"] is False


def test_remaining_ten_pages_unverified_and_immutable():
    original = ledger()
    rows = verify_page_five(original)
    assert rows[1:] == original[1:]
    assert all(row["status"] == "UNVERIFIED" for row in rows[1:])


def test_input_not_mutated():
    original = ledger()
    snapshot = json.dumps(original, sort_keys=True)
    verify_page_five(original)
    assert json.dumps(original, sort_keys=True) == snapshot


def test_run_outputs_complete_files(tmp_path):
    source = tmp_path / "input.tex"
    source.write_text(baseline(), encoding="utf-8")
    page_ledger = tmp_path / "ledger.json"
    page_ledger.write_text(json.dumps(ledger(), ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "result"
    summary = run(source, page_ledger, out)
    assert summary["status_counts"] == {"UNVERIFIED": 10, "CORRECTION_REQUIRED": 0, "VERIFIED": 1}
    assert summary["total_recorded_corrections"] == 15
    assert (out / "Toda_01_corrected.tex").read_text(encoding="utf-8") == baseline()
    assert (out / "page5_evidence.csv").exists()
    assert (out / "report.md").exists()


def test_unverified_chapter_and_no_production_changes(tmp_path):
    source = tmp_path / "input.tex"
    source.write_text(baseline(), encoding="utf-8")
    page_ledger = tmp_path / "ledger.json"
    page_ledger.write_text(json.dumps(ledger(), ensure_ascii=False), encoding="utf-8")
    result = run(source, page_ledger, tmp_path / "result")
    assert result["chapter_fully_verified"] is False
    assert result["statement_ids_changed"] == 0
    assert result["production_code_changed"] is False
    assert result["full_suite_run"] is False
