import json
from pathlib import Path

import pytest

from phase163_r4_r28_page5_alignment.align import (
    CHANGES,
    EXPECTED_SHA256,
    correct_page5,
    digest,
    run,
    update_ledger,
)

BASE = Path(__file__).resolve().parents[1]


def source_text():
    return (BASE / "R26_BASELINE.tex").read_text(encoding="utf-8")


def ledger_rows():
    return json.loads((BASE / "R27_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_hash():
    assert digest(source_text()) == EXPECTED_SHA256


def test_three_exact_changes():
    before = source_text()
    after = correct_page5(before)
    for _, old, new in CHANGES:
        assert old in before
        assert old not in after
        assert new in after


def test_preserves_all_other_text():
    before = source_text()
    for _, old, new in CHANGES:
        before = before.replace(old, new, 1)
    assert correct_page5(source_text()) == before


def test_no_double_application():
    with pytest.raises(ValueError):
        correct_page5(correct_page5(source_text()))


def test_changed_input_refused():
    with pytest.raises(ValueError):
        correct_page5(source_text() + "\n")


def test_ledger_only_page_one_updated():
    before = ledger_rows()
    after = update_ledger(before, EXPECTED_SHA256, "newsha")
    assert len(after) == 11
    assert after[0]["prior_corrections"] == before[0]["prior_corrections"] + 3
    assert after[0]["status"] == "UNVERIFIED"
    assert all(row["status"] == "UNVERIFIED" for row in after)
    assert all(row["source_sha256"] == "newsha" for row in after)
    assert before[0]["evidence_note"] == ""


def test_wrong_ledger_hash_refused():
    rows = ledger_rows()
    rows[1]["source_sha256"] = "invalid"
    with pytest.raises(ValueError):
        update_ledger(rows, EXPECTED_SHA256, "new")


def test_correct_run_keeps_input_and_writes_full_files(tmp_path):
    source = BASE / "R26_BASELINE.tex"
    ledger = BASE / "R27_PAGE_LEDGER.json"
    original = source.read_bytes()
    output = tmp_path / "out"
    summary = run(source, ledger, output)
    assert source.read_bytes() == original
    assert summary["total_recorded_corrections"] == 12
    assert summary["status_counts"]["VERIFIED"] == 0
    assert (output / "Toda_01_corrected.tex").read_text(encoding="utf-8") == correct_page5(source_text())
    assert len(json.loads((output / "page_ledger.json").read_text(encoding="utf-8"))) == 11


def test_wrong_source_creates_no_output(tmp_path):
    src = tmp_path / "bad.tex"
    src.write_text("wrong", encoding="utf-8")
    target = tmp_path / "out"
    with pytest.raises(ValueError):
        run(src, BASE / "R27_PAGE_LEDGER.json", target)
    assert not target.exists()
