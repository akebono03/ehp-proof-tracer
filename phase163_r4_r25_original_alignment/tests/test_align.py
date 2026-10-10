import hashlib
from pathlib import Path

import pytest

from phase163_r4_r25_original_alignment.align import (
    EXPECTED_SHA256,
    NEW,
    OLD,
    align,
    normalized_text,
    run,
)


def test_correction_is_exact_and_preserves_other_text():
    source = "start\n" + OLD + "\nend\n"
    assert align(source) == "start\n" + NEW + "\nend\n"


def test_missing_target_fails_closed():
    with pytest.raises(ValueError):
        align("irrelevant content")


def test_multiple_targets_fail_closed():
    with pytest.raises(ValueError):
        align(OLD + "\n" + OLD)


def test_already_corrected_fails_closed():
    with pytest.raises(ValueError):
        align(OLD + "\n" + NEW)


def test_r24_baseline_sha_and_correction():
    baseline = Path(__file__).resolve().parents[1] / "R24_BASELINE.tex"
    text = normalized_text(baseline)
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == EXPECTED_SHA256
    result = align(text)
    assert OLD not in result
    assert result.count(NEW) == 1


def test_run_produces_full_tex_and_report(tmp_path):
    baseline = Path(__file__).resolve().parents[1] / "R24_BASELINE.tex"
    summary = run(baseline, tmp_path)
    assert summary["confirmed_corrections"] == 1
    assert summary["chapter_fully_verified"] is False
    assert (tmp_path / "Toda_01_before_r25.tex").is_file()
    assert NEW in (tmp_path / "Toda_01_corrected.tex").read_text(encoding="utf-8")
    assert "PENDING_FULL_TEXT_COMPARISON" in (tmp_path / "alignment_review.csv").read_text(encoding="utf-8-sig")


def test_wrong_baseline_cannot_write_output(tmp_path):
    source = tmp_path / "wrong.tex"
    source.write_text(OLD, encoding="utf-8")
    out = tmp_path / "out"
    with pytest.raises(ValueError):
        run(source, out)
    assert not out.exists()
