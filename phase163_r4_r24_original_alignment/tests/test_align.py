from pathlib import Path
import pytest
from phase163_r4_r24_original_alignment.align import CORRECTIONS, align, run


SOURCE = Path(__file__).resolve().parents[2] / "phase163_r4_r23_preview" / "Toda_01_corrected.tex"


def sample_source():
    return "\n".join(row[3] for row in CORRECTIONS)


def test_corrects_both_pdf_confirmed_transcriptions():
    result = align(sample_source())
    for row in CORRECTIONS:
        assert row[4] in result
        assert row[3] not in result


def test_missing_correction_fails_closed():
    with pytest.raises(ValueError):
        align(CORRECTIONS[0][3])


def test_ambiguous_correction_fails_closed():
    with pytest.raises(ValueError):
        align(sample_source() + "\n" + CORRECTIONS[0][3])


def test_no_change_to_unrelated_text():
    source = "UNRELATED\n" + sample_source() + "\nUNCHANGED"
    result = align(source)
    assert result.startswith("UNRELATED\n")
    assert result.endswith("\nUNCHANGED")


def test_focused_full_file_corrections(tmp_path):
    source = tmp_path / "input.tex"
    repository_sample = Path(__file__).resolve().parents[1] / "R23_BASELINE.tex"
    source.write_bytes(repository_sample.read_bytes())
    summary = run(source, tmp_path / "output")
    assert summary["confirmed_corrections"] == 2
    assert summary["chapter_fully_verified"] is False
    assert summary["statement_ids_changed"] == 0
    assert (tmp_path / "output" / "Toda_01_before_r24.tex").read_text(encoding="utf-8") == source.read_text(encoding="utf-8")


def test_modified_input_is_rejected(tmp_path):
    file = tmp_path / "input.tex"
    file.write_text(sample_source(), encoding="utf-8")
    with pytest.raises(ValueError):
        run(file, tmp_path / "output")
