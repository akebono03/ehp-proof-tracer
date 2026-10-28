"""Focused tests for the complete, history-preserving document closeout."""
from __future__ import annotations

from pathlib import Path
import zipfile

import pytest

from phase169_r10et_closeout_r2_documentation.update_docs import (
    APPENDIX_PATHS,
    DOCUMENT_BLOBS,
    MARKER,
    README_ANCHOR,
    create_full_archive,
    updated_document,
)


@pytest.mark.parametrize("path", tuple(DOCUMENT_BLOBS))
def test_every_full_document_is_reconstructed_from_original(path: str):
    package = Path(__file__).resolve().parents[1]
    appendix = (package / "appendices" / APPENDIX_PATHS[path]).read_text(
        encoding="utf-8"
    )
    original = (
        b"# EHP Proof Tracer\n\n"
        + (README_ANCHOR + "\n\n").encode("utf-8")
        if path == "README.md"
        else b"# Original historical record\r\n\r\nHistorical content.\r\n"
    )
    output = updated_document(path, original, appendix)
    assert len(output) > len(original)
    if path == "README.md":
        assert output.startswith(b"# EHP Proof Tracer\n\n")
        assert output.endswith((README_ANCHOR + "\n\n").encode("utf-8"))
        assert "Phase 169 R10ET complete" in output.decode("utf-8")
    else:
        assert output.startswith(original)
        assert MARKER.encode("utf-8") in output
        assert output.count(MARKER.encode("utf-8")) == 1


def test_previous_development_and_proof_history_is_not_modified():
    for path in ("docs/development_log.md", "docs/proof_records.md"):
        package = Path(__file__).resolve().parents[1]
        appendix = (package / "appendices" / APPENDIX_PATHS[path]).read_text(
            encoding="utf-8"
        )
        original = b"# History\r\n\r\n\xff\x00"  # malformed original must fail
        with pytest.raises(UnicodeDecodeError):
            updated_document(path, original, appendix)
        valid = b"# History\r\n\r\n\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e\r\n"
        assert updated_document(path, valid, appendix).startswith(valid)


def test_unsafe_or_duplicate_updates_fail_closed():
    original = ("# Head\n" + README_ANCHOR + "\n").encode("utf-8")
    appendix = "## Current status — Phase 169 R10ET complete; Phase 169 remains open\n"
    updated = updated_document("README.md", original, appendix)
    with pytest.raises(ValueError, match="already updated"):
        updated_document("README.md", updated, appendix)
    with pytest.raises(ValueError, match="missing or ambiguous"):
        updated_document("README.md", b"# Missing heading\n", appendix)
    with pytest.raises(ValueError, match="Unexpected document"):
        updated_document("another.md", b"# Some record\n", appendix)
    with pytest.raises(ValueError, match="Missing append-only"):
        updated_document("docs/design.md", b"# Design\n", "## Missing marker\n")


def test_appendix_languages_and_safety_boundaries():
    package = Path(__file__).resolve().parents[1] / "appendices"
    readme = (package / APPENDIX_PATHS["README.md"]).read_text(encoding="utf-8")
    assert "Phase 169 remains open" in readme
    assert "formal verification" in readme
    for path in DOCUMENT_BLOBS:
        appendix = (package / APPENDIX_PATHS[path]).read_text(encoding="utf-8")
        assert "Phase 169" in appendix
        assert "19" in appendix
        assert "pytest" in appendix
        if path != "README.md":
            assert appendix.startswith(MARKER)
            assert "全体 pytest" in appendix


def test_complete_archive_contains_only_five_full_document_files(tmp_path: Path):
    payloads: dict[str, bytes] = {}
    for index, path in enumerate(DOCUMENT_BLOBS):
        target = tmp_path / "AFTER_FULL" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = (
            b"# Full updated record\n"
            if index % 2 == 0
            else b"# Full updated record\r\n"
        )
        target.write_bytes(payload)
        payloads[path] = payload
    archive = create_full_archive(tmp_path)
    assert archive.exists()
    with zipfile.ZipFile(archive, "r") as f:
        assert set(f.namelist()) == set(DOCUMENT_BLOBS)
        for path in DOCUMENT_BLOBS:
            assert f.read(path) == payloads[path]


def test_local_git_end_to_end_document_write_and_index_preserved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import subprocess
    import phase169_r10et_closeout_r2_documentation.update_docs as module

    root = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "develop", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "test"], check=True)
    for path in DOCUMENT_BLOBS:
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        text = "# EHP Proof Tracer\n\n" + README_ANCHOR + "\n" if path == "README.md" else "# 記録\n\n過去の本文。\n"
        file.write_text(text, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "README.md", "docs"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "baseline"], check=True)
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(remote)], check=True)
    subprocess.run(["git", "-C", str(root), "push", "-q", "-u", "origin", "develop"], check=True)
    head = module.git(root, "rev-parse", "HEAD")
    blobs = {path: module.git(root, "hash-object", f"--path={path}", path)
             for path in DOCUMENT_BLOBS}
    monkeypatch.setattr(module, "REVIEWED_HEAD", head)
    monkeypatch.setattr(module, "DOCUMENT_BLOBS", blobs)
    monkeypatch.setattr(module, "REVIEWED_SOURCE_BLOBS", {})
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    for path in DOCUMENT_BLOBS:
        assert module.git(root, "hash-object", f"--path={path}", path) == blobs[path]
    before = {path: (root / path).read_bytes() for path in DOCUMENT_BLOBS}
    assert module.execute(root, Path(__file__).resolve().parents[1]) == 0
    changed = set(module.git(root, "diff", "--name-only").splitlines())
    assert changed == set(DOCUMENT_BLOBS)
    assert not module.git(root, "diff", "--cached", "--name-only")
    for path in DOCUMENT_BLOBS:
        updated = (root / path).read_bytes()
        assert len(updated) > len(before[path])
        if path != "README.md":
            assert updated.startswith(before[path])
    exported = list((tmp_path / "localappdata" / "EHPProofTracerRecovery").glob("r10et_closeout_r2_*/updated_five_documents_FULL.zip"))
    assert len(exported) == 1
    with zipfile.ZipFile(exported[0]) as documents:
        for path in DOCUMENT_BLOBS:
            assert documents.read(path) == (root / path).read_bytes()
    with pytest.raises(ValueError):
        module.updated_document("docs/design.md", (root / "docs/design.md").read_bytes(),
                                (Path(__file__).resolve().parents[1] / "appendices" / "design_append.md").read_text(encoding="utf-8"))
