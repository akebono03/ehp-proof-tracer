"""Document-only regression checks; no full mathematical test suite."""
from __future__ import annotations

import pytest

from phase172_r6r2_document_closeout.sections import (
    APPENDS, DESIGN_ADDENDUM, DEVELOPMENT_ADDENDUM, MARKER,
    PROOF_ADDENDUM, README_CURRENT, ROADMAP_ADDENDUM, make_revision,
)
from phase172_r6r2_document_closeout.install import DOC_BLOBS


def test_complete_readme_revision_preserves_history_and_updates_current():
    old = (
        "# EHP Proof Tracer\n\nIntroduction.\n\n"
        "<!-- PHASE171_FINAL_CLOSEOUT_20261031 -->\n\n"
        "## Current status — Phase 171 closed (2026-10-31)\n"
        "Older text.\n"
    ).encode("utf-8")
    updated = make_revision("README.md", old)
    assert updated.startswith(b"# EHP Proof Tracer")
    assert b"Older text." in updated
    assert MARKER.encode() in updated
    assert b"3546 passed in 107.52s" in updated
    assert "Historical closeout" in updated.decode("utf-8")
    assert "Phase 172 closed" in updated.decode("utf-8")
    assert len(updated) > len(old)


def test_append_revisions_preserve_every_original_byte():
    original = "# 日本語の記録\r\n\r\n過去の段落\r\n".encode("utf-8")
    for path in APPENDS:
        updated = make_revision(path, original)
        assert updated.startswith(original)
        assert MARKER.encode("utf-8") in updated
        assert b"\r\n" in updated
        assert len(updated) > len(original)


def test_unfinished_or_duplicated_closeout_is_rejected():
    with pytest.raises(ValueError):
        make_revision("docs/roadmap.md", MARKER.encode("utf-8"))
    with pytest.raises(ValueError):
        make_revision("README.md", b"# Invalid README\n")
    with pytest.raises(ValueError):
        make_revision("docs/unknown.md", b"# Unknown\n")


def test_required_phase_boundaries_and_reference_trust_remain_explicit():
    assert "ADOPTED_DATABASE_PRIOR" in DESIGN_ADDENDUM
    assert "ADOPTED_DATABASE_PRIOR" in PROOF_ADDENDUM
    assert "independently authenticated" in README_CURRENT
    assert "全体 pytest を**1回**" in DEVELOPMENT_ADDENDUM
    assert "次 Phase は未決定" in ROADMAP_ADDENDUM


def test_exactly_five_reviewed_document_paths():
    assert set(DOC_BLOBS) == {"README.md", *APPENDS}
    assert len(DOC_BLOBS) == 5


def test_additional_document_text_is_utf8_and_not_abridged():
    for path, text in APPENDS.items():
        assert path.startswith("docs/")
        assert MARKER in text
        assert len(text.encode("utf-8")) > 500
        assert "Phase 172" in text
    assert "Phase 172" in README_CURRENT
