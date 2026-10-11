import json
from pathlib import Path

import pytest

from phase163_r4_r38_page7_verification.verify import (
    EVIDENCE,
    EXPECTED_SHA256,
    run,
    sha256,
    validate_inputs,
    verify_page_seven,
)


ROOT = Path(__file__).resolve().parents[1]


def fixtures():
    text = (ROOT / "R37_BASELINE.tex").read_text(encoding="utf-8")
    ledger = json.loads((ROOT / "R37_PAGE_LEDGER.json").read_text(encoding="utf-8"))
    normalization = json.loads((ROOT / "R37_SOURCE_NORMALIZATION.json").read_text(encoding="utf-8"))
    return text, ledger, normalization


def test_baseline_sha256():
    text, ledger, normalization = fixtures()
    assert sha256(text) == EXPECTED_SHA256
    validate_inputs(text, ledger, normalization)


def test_rejects_modified_source():
    text, ledger, normalization = fixtures()
    with pytest.raises(ValueError, match="SHA-256"):
        validate_inputs(text + " ", ledger, normalization)


def test_rejects_invalid_ledger():
    text, ledger, normalization = fixtures()
    ledger.pop()
    with pytest.raises(ValueError, match="Eleven-page"):
        validate_inputs(text, ledger, normalization)


def test_rejects_missing_normalization():
    text, ledger, normalization = fixtures()
    normalization["record_key"] = "different"
    with pytest.raises(ValueError, match="normalization"):
        validate_inputs(text, ledger, normalization)


def test_page7_mathematically_verified_not_verbatim():
    text, ledger, normalization = fixtures()
    result = verify_page_seven(text, ledger, normalization)
    assert result[2]["status"] == "VERIFIED"
    assert result[2]["verbatim_transcription_verified"] is False
    assert result[2]["original_typo_confirmed"] is False
    assert result[2]["verification_scope"].endswith("SOURCE_NORMALIZATION")


def test_exception_retained_and_no_proof_search():
    text, ledger, normalization = fixtures()
    page = verify_page_seven(text, ledger, normalization)[2]
    exception = page["unresolved_original_discrepancies"][0]
    assert exception["original_printed"] != exception["current_tex"]
    assert exception["proof_search_eligible"] is False
    assert exception["auto_corrected"] is False


def test_other_page_statuses_preserved():
    text, ledger, normalization = fixtures()
    result = verify_page_seven(text, ledger, normalization)
    assert [x["status"] for x in result] == ["VERIFIED"] * 3 + ["UNVERIFIED"] * 8
    assert result[:2] == ledger[:2]
    assert result[3:] == ledger[3:]


def test_evidence_covers_nine_topics():
    assert len(EVIDENCE) == 9
    assert sum(row[2] == "NORMALIZED_EXCEPTION" for row in EVIDENCE) == 1


def test_run_writes_utf8_and_summary(tmp_path):
    text, ledger, normalization = fixtures()
    source = tmp_path / "in.tex"
    source.write_text(text, encoding="utf-8")
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
    normalization_path = tmp_path / "normalization.json"
    normalization_path.write_text(json.dumps(normalization, ensure_ascii=False), encoding="utf-8")
    summary = run(source, ledger_path, normalization_path, tmp_path / "out")
    assert summary["status_counts"]["VERIFIED"] == 3
    assert summary["total_recorded_corrections"] == 18
    assert (tmp_path / "out" / "Toda_01_corrected.tex").read_text(encoding="utf-8") == text
    assert (tmp_path / "out" / "page7_evidence.csv").exists()
    assert (tmp_path / "out" / "source_normalization.json").exists()
