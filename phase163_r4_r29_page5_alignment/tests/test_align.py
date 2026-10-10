import json
from pathlib import Path

import pytest

from phase163_r4_r29_page5_alignment.align import (
    CHANGES,
    EXPECTED_SHA256,
    align,
    digest,
    run,
    update_ledger,
)

ROOT = Path(__file__).resolve().parents[1]


def baseline():
    return (ROOT / "R28_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((ROOT / "R28_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_sha():
    assert digest(baseline()) == EXPECTED_SHA256


def test_original_phrases_are_unique():
    text = baseline()
    for key, before, after, evidence in CHANGES:
        assert text.count(before) == 1, key
        assert after not in text
        assert evidence


def test_align_changes_only_expected_text():
    expected = baseline()
    for key, before, after, evidence in CHANGES:
        expected = expected.replace(before, after, 1)
    assert align(baseline()) == expected


def test_align_rejects_wrong_sha():
    with pytest.raises(ValueError, match="SHA-256"):
        align(baseline() + " ")


def test_align_rejects_repeat():
    with pytest.raises(ValueError, match="SHA-256"):
        align(align(baseline()))


def test_ledger_all_pages_preserved():
    updated = update_ledger(ledger(), EXPECTED_SHA256, digest(align(baseline())))
    assert len(updated) == 11
    assert all(row["status"] == "UNVERIFIED" for row in updated)
    assert updated[0]["prior_corrections"] == ledger()[0]["prior_corrections"] + 2
    assert updated[1]["prior_corrections"] == ledger()[1]["prior_corrections"]


def test_ledger_rejects_wrong_source():
    with pytest.raises(ValueError, match="hash mismatch"):
        update_ledger(ledger(), "wrong", "new")


def test_run_generates_full_text_and_reports(tmp_path):
    source = tmp_path / "source.tex"
    source.write_text(baseline(), encoding="utf-8")
    summary = run(source, ROOT / "R28_PAGE_LEDGER.json", tmp_path / "out")
    assert summary["confirmed_corrections"] == 2
    assert summary["total_recorded_corrections"] == 14
    assert summary["status_counts"]["VERIFIED"] == 0
    assert (tmp_path / "out" / "Toda_01_corrected.tex").read_text(encoding="utf-8") == align(baseline())
    assert (tmp_path / "out" / "Toda_01_before_r29.tex").read_text(encoding="utf-8") == baseline()


def test_run_refuses_modified_source_without_outputs(tmp_path):
    source = tmp_path / "wrong.tex"
    source.write_text(baseline() + "extra", encoding="utf-8")
    destination = tmp_path / "out"
    with pytest.raises(ValueError):
        run(source, ROOT / "R28_PAGE_LEDGER.json", destination)
    assert not destination.exists()
