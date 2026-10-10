from pathlib import Path

import pytest

from phase163_r4_r23_original_alignment.align import OLD, NEW, align, run


def test_replaces_exactly_one_verified_parenthesis():
    assert align("A" + OLD + "B") == "A" + NEW + "B"


def test_preserves_unrelated_text():
    assert align("unchanged\n" + OLD + "\nending").startswith("unchanged\n")


def test_rejects_missing_target():
    with pytest.raises(ValueError):
        align("other equation")


def test_rejects_duplicate_target():
    with pytest.raises(ValueError):
        align(OLD + OLD)


def test_refuses_unexpected_source(tmp_path: Path):
    source = tmp_path / "wrong.tex"
    source.write_text(OLD, encoding="utf-8")
    with pytest.raises(ValueError):
        run(source, tmp_path / "out")
    assert not (tmp_path / "out").exists()
