import hashlib
from pathlib import Path

import pytest

from phase163_r4_r26_original_alignment.align import (
    EXPECTED_SHA256,
    NEW,
    OLD,
    START_MARKER,
    PROOF_MARKER,
    align,
    normalized_text,
    run,
)


def fixture_source(proof: str) -> str:
    return "header\n" + START_MARKER + "\nstatement\n\\end{proposition}\n" + PROOF_MARKER + proof


def test_exact_two_occurrences_in_proof_are_repaired():
    source = fixture_source("A " + OLD + " B " + OLD + " C")
    result = align(source)
    assert result == fixture_source("A " + NEW + " B " + NEW + " C")


def test_missing_and_extra_targets_fail_closed():
    for text in ("none", OLD, OLD + OLD + OLD):
        with pytest.raises(ValueError):
            align(fixture_source(text))


def test_already_corrected_target_fails_closed():
    with pytest.raises(ValueError):
        align(fixture_source(OLD + NEW + OLD))


def test_wrong_proposition_boundary_fails_closed():
    with pytest.raises(ValueError):
        align(OLD + OLD)


def test_other_regions_not_modified():
    source = fixture_source("A " + OLD + " B " + OLD + " C")
    result = align(source)
    assert source.split(START_MARKER)[0] == result.split(START_MARKER)[0]
    assert source.split(PROOF_MARKER)[0] == result.split(PROOF_MARKER)[0]


def test_known_r25_baseline_sha_and_repair():
    baseline = Path(__file__).resolve().parents[1] / "R25_BASELINE.tex"
    source = normalized_text(baseline)
    assert hashlib.sha256(source.encode("utf-8")).hexdigest() == EXPECTED_SHA256
    result = align(source)
    assert result.count(NEW) == 2
    assert OLD not in result


def test_run_writes_full_tex_and_review(tmp_path):
    baseline = Path(__file__).resolve().parents[1] / "R25_BASELINE.tex"
    summary = run(baseline, tmp_path)
    assert summary["confirmed_corrections"] == 2
    assert summary["chapter_fully_verified"] is False
    assert (tmp_path / "Toda_01_before_r26.tex").is_file()
    assert (tmp_path / "Toda_01_corrected.tex").read_text(encoding="utf-8").count(NEW) == 2
    assert "PENDING_FULL_TEXT_COMPARISON" in (tmp_path / "alignment_review.csv").read_text(encoding="utf-8-sig")


def test_wrong_sha_leaves_output_unwritten(tmp_path):
    source = tmp_path / "wrong.tex"
    source.write_text(fixture_source(OLD + OLD), encoding="utf-8")
    target = tmp_path / "out"
    with pytest.raises(ValueError):
        run(source, target)
    assert not target.exists()
