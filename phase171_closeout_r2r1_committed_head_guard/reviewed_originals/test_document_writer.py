"""Pure checks for history-safe full-document replacement and source boundaries."""
from __future__ import annotations

import pytest

from phase171_closeout_r2_documentation_full_output.update_docs import (
    DOC_BLOBS,
    MARKER,
    README_ANCHOR,
    updated_document,
    section_text,
    SECTIONS,
)


@pytest.mark.parametrize("relative", tuple(DOC_BLOBS))
def test_generates_complete_documents_without_erasing_history(relative: str):
    if relative == "README.md":
        old = ("# EHP Proof Tracer\n\n" + README_ANCHOR
               + "\n\n## Phase 170 historical content\n").encode("utf-8")
    else:
        old = ("# 昔の記録\n\n歴史的な説明を保持する。\n" + relative + "\n").encode("utf-8")
    new = updated_document(relative, old)
    assert new != old
    assert b"Phase 171" in new
    if relative == "README.md":
        assert new.startswith(b"# EHP Proof Tracer\n\n")
        assert new.endswith(b"## Phase 170 historical content\n")
        assert new.count(MARKER.encode("ascii")) == 1
    else:
        assert new.startswith(old)
        assert old in new
        assert "Phase 171" in section_text(SECTIONS[relative])


def test_readme_fails_closed_without_reviewed_anchor():
    with pytest.raises(ValueError, match="anchor"):
        updated_document("README.md", b"# Not the reviewed README\n")


def test_duplicate_document_update_is_refused():
    old = ("# EHP Proof Tracer\n" + README_ANCHOR + "\n").encode("utf-8")
    updated = updated_document("README.md", old)
    with pytest.raises(ValueError, match="already exists"):
        updated_document("README.md", updated)


def test_crlf_and_bom_preserved_for_append_only_document():
    old = b"\xef\xbb\xbf" + "# 日本語記録\r\n\r\n過去の本文。\r\n".encode("utf-8")
    new = updated_document("docs/proof_records.md", old)
    assert new.startswith(old)
    assert b"\r\n" in new
    assert b"\n" not in new.replace(b"\r\n", b"")


def test_other_paths_refused():
    with pytest.raises(ValueError, match="unreviewed"):
        updated_document("README_OTHER.md", b"# Not reviewed\n")


def test_no_phase_end_full_pytest_claim():
    for relative in DOC_BLOBS:
        content = section_text(SECTIONS[relative])
        assert "Phase 171" in content
        assert "pytest" in content
        assert "88" in content
    readme = section_text("readme.md")
    assert "has **not** yet been run" in readme


def test_guarded_full_document_end_to_end_on_local_fixture(tmp_path, monkeypatch):
    """A fixture repository exercises Git guards, byte retention and complete ZIP."""
    import hashlib
    import os
    from pathlib import Path
    import subprocess
    import zipfile
    from phase171_closeout_r2_documentation_full_output import update_docs as module

    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    subprocess.run(["git", "init", "-b", "develop", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "test"], check=True)
    originals = {}
    for relative in DOC_BLOBS:
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative == "README.md":
            source = ("# EHP Proof Tracer\n\n" + README_ANCHOR + "\n## Historical\n").encode("utf-8")
        else:
            source = ("# 過去の文書\n\n" + relative + "\n").encode("utf-8")
        path.write_bytes(source)
        originals[relative] = source
    test_file = repo / module.R1R1_TEST
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_bytes(b"# historical test\n")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "baseline"], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
    subprocess.run(["git", "-C", str(repo), "push", "-q", "-u", "origin", "develop"], check=True)
    def repo_git(*args):
        return subprocess.run(["git", "-C", str(repo), *args],
                              check=True, capture_output=True, text=True).stdout.strip()
    reviewed_head = repo_git("rev-parse", "HEAD")
    blobs = {relative: repo_git("rev-parse", "HEAD:" + relative) for relative in DOC_BLOBS}
    old_test_sha = repo_git("rev-parse", "HEAD:" + module.R1R1_TEST)
    revised = b"# semantic proof preservation test\n"
    test_file.write_bytes(revised)
    monkeypatch.setattr(module, "ROOT", repo)
    monkeypatch.setattr(module, "EXPECTED_HEAD", reviewed_head)
    monkeypatch.setattr(module, "DOC_BLOBS", blobs)
    monkeypatch.setattr(module, "R1R1_SOURCE_BLOB", old_test_sha)
    monkeypatch.setattr(module, "R1R1_EXPECTED", hashlib.sha256(revised).hexdigest())
    monkeypatch.setattr(module, "FOCUSED", ())
    monkeypatch.setattr(module, "run_focused", lambda: {"exit_code": 0, "output": "fixture pass"})
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    monkeypatch.setattr("sys.argv", ["update_docs.py"])
    assert module.main() == 0
    changed = set(repo_git("diff", "--name-only", "HEAD", "--").splitlines())
    assert changed == set(DOC_BLOBS) | {module.R1R1_TEST}
    for relative in DOC_BLOBS:
        actual = (repo / relative).read_bytes()
        assert actual == module.updated_document(relative, originals[relative])
        if relative != "README.md":
            assert actual.startswith(originals[relative])
    archives = list((tmp_path / "localappdata" / "EHPProofTracerRecovery").glob("*/PHASE171_R2_FIVE_FULL_DOCUMENTS.zip"))
    assert len(archives) == 1
    with zipfile.ZipFile(archives[0]) as handle:
        for relative in DOC_BLOBS:
            assert handle.read(relative) == (repo / relative).read_bytes()
    assert module.main() == 0
