from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase163_r4_r30_page5_alignment.align import (
    EXPECTED_SHA256, NEW, OLD, correct_page5, digest, run, update_ledger,
)

PACKAGE = Path(__file__).resolve().parents[1]


def baseline() -> str:
    return (PACKAGE / "R29_BASELINE.tex").read_text(encoding="utf-8")


def ledger() -> list[dict]:
    return json.loads((PACKAGE / "R29_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_input_hash_matches_baseline():
    assert digest(baseline()) == EXPECTED_SHA256


def test_original_formula_occurs_exactly_once():
    assert baseline().count(OLD) == 1


def test_correction_is_limited_to_one_formula():
    text = baseline()
    assert correct_page5(text) == text.replace(OLD, NEW, 1)


def test_corrected_formula_is_present_once():
    assert correct_page5(baseline()).count(NEW) == 1


def test_second_attempt_is_rejected():
    with pytest.raises(ValueError, match="SHA-256"):
        correct_page5(correct_page5(baseline()))


def test_ledger_pages_remain_unverified():
    pages = update_ledger(ledger(), EXPECTED_SHA256, digest(correct_page5(baseline())))
    assert len(pages) == 11
    assert all(p["status"] == "UNVERIFIED" for p in pages)


def test_prior_corrections_increment_one():
    pages = update_ledger(ledger(), EXPECTED_SHA256, digest(correct_page5(baseline())))
    assert pages[0]["prior_corrections"] == ledger()[0]["prior_corrections"] + 1
    assert pages[1]["prior_corrections"] == ledger()[1]["prior_corrections"]


def test_incorrect_ledger_hash_is_rejected():
    data = ledger()
    data[2]["source_sha256"] = "incorrect"
    with pytest.raises(ValueError, match="hash or status"):
        update_ledger(data, EXPECTED_SHA256, "abc")


def test_run_writes_complete_files(tmp_path):
    source = tmp_path / "input.tex"
    source.write_text(baseline(), encoding="utf-8")
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(json.dumps(ledger()), encoding="utf-8")
    summary = run(source, ledger_path, tmp_path / "out")
    assert summary["total_recorded_corrections"] == 15
    assert summary["status_counts"]["VERIFIED"] == 0
    assert (tmp_path / "out" / "Toda_01_corrected.tex").read_text(encoding="utf-8") == correct_page5(baseline())
    assert (tmp_path / "out" / "alignment_review.csv").exists()
    assert (tmp_path / "out" / "report.md").exists()
