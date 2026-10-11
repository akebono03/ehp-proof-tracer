import json
from pathlib import Path

import pytest

from phase163_r4_r32_page6_alignment.align import (
    AFTER,
    BEFORE,
    EXPECTED_SHA256,
    correct_page_six,
    digest,
    run,
    update_ledger,
)


HERE = Path(__file__).resolve().parents[1]


def baseline():
    return (HERE / "R31_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((HERE / "R31_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_hash():
    assert digest(baseline()) == EXPECTED_SHA256


def test_source_contains_single_target():
    assert baseline().count(BEFORE) == 1


def test_correction_restores_original_sphere_coherence():
    text = correct_page_six(baseline())
    assert AFTER in text
    assert r"\shrink_{m+n,p}" in text
    assert r"\shrink_{m,n+p}" in text


def test_correction_preserves_equation_13():
    text = correct_page_six(baseline())
    assert r"\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}" in text


def test_source_mismatch_fails():
    with pytest.raises(ValueError, match="SHA-256"):
        correct_page_six(baseline() + "changed")


def test_ledger_updates_only_page6_review_state():
    result = update_ledger(ledger(), "new-hash")
    assert result[0]["status"] == "VERIFIED"
    assert result[1]["status"] == "UNVERIFIED"
    assert all(x["status"] == "UNVERIFIED" for x in result[2:])
    assert all(x["source_sha256"] == "new-hash" for x in result)


def test_ledger_invalid_state_fails():
    data = ledger()
    data[2]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="status"):
        update_ledger(data, "sha")


def test_run_writes_utf8_full_files(tmp_path):
    summary = run(HERE / "R31_BASELINE.tex", HERE / "R31_PAGE_LEDGER.json", tmp_path)
    assert summary["total_recorded_corrections"] == 16
    assert summary["status_counts"] == {"VERIFIED": 1, "UNVERIFIED": 10, "CORRECTION_REQUIRED": 0}
    assert (tmp_path / "Toda_01_corrected.tex").read_text(encoding="utf-8") == correct_page_six(baseline())
    assert (tmp_path / "alignment_review.csv").exists()
