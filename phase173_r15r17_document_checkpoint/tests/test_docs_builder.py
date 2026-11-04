"""Focused full-document transformation contracts; no repository dependencies."""
from __future__ import annotations

import pytest

from phase173_r15r17_document_checkpoint.docs_builder import (
    APPENDS,
    DOCUMENT_BLOBS,
    MARKER,
    apply_document_update,
)


def test_five_canonical_documents_selected() -> None:
    assert set(DOCUMENT_BLOBS) == {
        "README.md", "docs/design.md", "docs/development_log.md",
        "docs/roadmap.md", "docs/proof_records.md",
    }


def test_readme_full_text_keeps_history_and_changes_current_heading() -> None:
    raw = (
        "# EHP Proof Tracer\n\nIntro.\n\n"
        "<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->\n\n"
        "## Current status — Phase 172 closed (2026-10-31)\n\nHistory.\n"
    ).encode("utf-8")
    out = apply_document_update("README.md", raw)
    text = out.decode("utf-8")
    assert text.count(MARKER) == 1
    assert "Intro." in text and "History." in text
    assert "## Historical closeout — Phase 172" in text
    assert "## Current status — Phase 173 R15R17" in text
    assert "full suite" in text
    assert "No Phase 173 full-suite result" in text


@pytest.mark.parametrize("path", tuple(APPENDS))
def test_japanese_doc_appends_whole_content_and_preserves_history(path: str) -> None:
    raw = ("# EHP Proof Tracer " + path + "\n\n歴史的な記録。\n").encode("utf-8")
    updated = apply_document_update(path, raw)
    assert updated.startswith(raw)
    assert updated.count(MARKER.encode("utf-8")) == 1
    assert len(updated) > len(raw)
    if path in ("docs/design.md", "docs/roadmap.md", "docs/proof_records.md"):
        assert b"\\pi" in updated


def test_design_preserves_existing_crlf_full_file() -> None:
    raw = b"# EHP Proof Tracer\r\n\r\nOld material.\r\n"
    out = apply_document_update("docs/design.md", raw)
    assert out.startswith(raw)
    assert b"\r\n<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->" in out


def test_duplicate_checkpoint_marker_fails_closed() -> None:
    raw = f"# EHP Proof Tracer\n\n{MARKER}\n".encode("utf-8")
    with pytest.raises(ValueError, match="already applied"):
        apply_document_update("docs/roadmap.md", raw)


def test_readme_unreviewed_anchor_fails_closed() -> None:
    with pytest.raises(ValueError, match="unreviewed README anchor"):
        apply_document_update("README.md", b"# EHP Proof Tracer\n")


def test_unreviewed_target_fails_closed() -> None:
    with pytest.raises(ValueError, match="unreviewed document path"):
        apply_document_update("docs/other.md", b"# EHP Proof Tracer\n")


def test_full_five_files_are_written_and_git_index_preserved(tmp_path, monkeypatch) -> None:
    """Exercise the actual installer with a disposable Git repository."""
    import subprocess
    from pathlib import Path

    import phase173_r15r17_document_checkpoint.docs_builder as builder

    repo: Path = tmp_path / "repository"
    repo.mkdir()

    def execute(*args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True,
            check=True, encoding="utf-8",
        )
        return completed.stdout.strip()

    execute("init", "-q", "-b", "develop")
    execute("config", "user.name", "Documentation Gate")
    execute("config", "user.email", "gate@example.invalid")
    originals: dict[str, bytes] = {}
    for path in DOCUMENT_BLOBS:
        filename = repo / path
        filename.parent.mkdir(parents=True, exist_ok=True)
        original = (
            b"# EHP Proof Tracer\n\n"
            b"<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->\n\n"
            b"## Current status \xe2\x80\x94 Phase 172 closed (2026-10-31)\n"
            if path == "README.md" else
            b"# EHP Proof Tracer\n\nEarlier proof notes.\n"
        )
        filename.write_bytes(original)
        originals[path] = original
    execute("add", "README.md", "docs")
    execute("commit", "-q", "-m", "baseline")
    head = execute("rev-parse", "HEAD")
    execute("update-ref", "refs/remotes/origin/develop", head)
    monkeypatch.setattr(builder, "REVIEWED_BASE", head)
    monkeypatch.setattr(
        builder, "DOCUMENT_BLOBS",
        {path: execute("rev-parse", f"HEAD:{path}") for path in DOCUMENT_BLOBS},
    )
    package = repo / "phase173_r15r17_document_checkpoint"
    (package / "tests").mkdir(parents=True)
    before = execute("ls-files", "--stage")
    builder.generate_files(repo, package, apply=False)
    assert execute("ls-files", "--stage") == before
    for path, original in originals.items():
        assert (repo / path).read_bytes() == original
        assert MARKER.encode("utf-8") in (package / "full_documents" / path).read_bytes()
    builder.generate_files(repo, package, apply=True)
    assert execute("ls-files", "--stage") == before
    for path, original in originals.items():
        assert (package / "original_backups" / path).read_bytes() == original
        assert (repo / path).read_bytes() == (package / "full_documents" / path).read_bytes()
    with pytest.raises(RuntimeError, match="unreviewed changes"):
        builder.generate_files(repo, package, apply=True)
