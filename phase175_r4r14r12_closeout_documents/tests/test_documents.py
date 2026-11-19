"""Focused, source-independent document transformation tests."""
from __future__ import annotations

import pytest

from phase175_r4r14r12_closeout_documents.build_documents import (
    DOCUMENT_BLOBS, MARKER, NOTES, render_full,
)


@pytest.mark.parametrize("path", sorted(DOCUMENT_BLOBS))
def test_complete_original_history_preserved(path: str) -> None:
    original = "# Example\n\nPrior historical record.\n\n## Earlier phase\nOld result.\n"
    generated = render_full(path, original)
    assert generated.startswith("# Example\n")
    assert "Prior historical record." in generated
    assert "## Earlier phase\nOld result." in generated
    assert MARKER in generated
    assert len(generated) > len(original)
    assert NOTES[path] in generated


@pytest.mark.parametrize("path", sorted(DOCUMENT_BLOBS))
def test_repeat_generation_fails_closed(path: str) -> None:
    once = render_full(path, "# Example\nOld text.\n")
    with pytest.raises(ValueError, match="ALREADY_UPDATED"):
        render_full(path, once)


def test_missing_title_fails_closed() -> None:
    with pytest.raises(ValueError, match="DOCUMENT_TITLE_MISSING"):
        render_full("README.md", "There is no title\n")


def test_readme_in_english_and_other_notes_in_japanese() -> None:
    assert "Current development status" in NOTES["README.md"]
    assert "現行設計境界" in NOTES["docs/design.md"]
    assert "終了前に残る義務" in NOTES["docs/roadmap.md"]
    assert "開発" not in NOTES["README.md"]
