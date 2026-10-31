# Phase 171 Closeout R2R3 — 変更コード全文

## 変更対象

- `phase171_closeout_r2_documentation_full_output/update_docs.py`
- `phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py`

変更後の **両ファイル全文** は `replacements/` にある。以下は変更する import 領域と関数の省略のない全文。

## update_docs.py の import 領域全文

```python
"""Phase 171 Closeout R2: guarded five-document full-file writer.

The reviewed repository files are read from the user's checked-out worktree.
All five complete revised files are exported. No full pytest is invoked.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile
```

## `lf_text()` 関数全文

```python
def lf_text(data: bytes) -> str:
    """Normalize one or more CR bytes followed by LF for comparison only.

    Historical documents may contain CRCRLF, CRLF, and LF together. A bare CR
    is not treated as a line ending, because silently changing it could alter
    a historical record.
    """
    value = data.decode("utf-8-sig")
    value = re.sub(r"\r+\n", "\n", value)
    if "\r" in value:
        raise ValueError("unknown line endings")
    return value
```

## `document_newline()` 関数全文

```python
def document_newline(original: bytes) -> bytes:
    """Choose the final existing line separator, without changing old bytes."""
    index = original.rfind(b"\n")
    if index < 0:
        return b"\n"
    start = index
    while start > 0 and original[start - 1] == 13:
        start -= 1
    return original[start:index + 1]
```

## `updated_document()` 関数全文

```python
def updated_document(relative: str, original: bytes) -> bytes:
    """Generate a complete new file, preserving every historical source byte."""
    if relative not in DOC_BLOBS:
        raise ValueError("unreviewed document path")
    text = lf_text(original)
    section = section_text(SECTIONS[relative])
    if MARKER in text:
        raise ValueError("Phase 171 documentation marker already exists")
    if "Phase 171" not in section or "pytest" not in section:
        raise ValueError("reviewed Phase 171 section contract failed")
    newline = document_newline(original)
    section_bytes = section.encode("utf-8").replace(b"\n", newline)
    if relative == "README.md":
        anchor = README_ANCHOR + "\n"
        if text.count(anchor) != 1 or not section.startswith("<!-- " + MARKER + " -->"):
            raise ValueError("README insertion anchor missing or ambiguous")
        anchor_bytes = README_ANCHOR.encode("utf-8")
        if original.count(anchor_bytes) != 1:
            raise ValueError("README insertion anchor missing or ambiguous")
        position = original.index(anchor_bytes)
        changed = original[:position] + section_bytes + original[position:]
    else:
        if not (section.startswith("\n## ") or section.startswith("\n\n## ")):
            raise ValueError("append-only section marker missing")
        changed = original + section_bytes
    if lf_text(changed).count(MARKER) != (1 if relative == "README.md" else 0):
        raise ValueError("Phase 171 marker count invalid")
    if relative != "README.md" and not changed.startswith(original):
        raise ValueError("historical bytes not preserved")
    return changed
```

## `current_files()` 関数全文

```python
def current_files() -> tuple[dict[str, bytes], dict[str, bytes], set[str]]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if head != EXPECTED_HEAD:
        try:
            git("merge-base", "--is-ancestor", EXPECTED_HEAD, "HEAD")
        except subprocess.CalledProcessError as exc:
            raise RuntimeError("local HEAD is not descended from reviewed base") from exc
        committed_delta = {
            path for path in git(
                "diff", "--name-only", EXPECTED_HEAD, "HEAD", "--"
            ).splitlines() if path
        }
        allowed_delta = {
            path for path in committed_delta
            if path == R1R1_TEST
            or path.startswith("phase171_closeout_r1_preflight_audit/")
            or path.startswith("phase171_closeout_r1r1_r3z_semantic_guard/")
        }
        if committed_delta != allowed_delta:
            raise RuntimeError(
                "unreviewed committed paths after reviewed base HEAD: "
                + ", ".join(sorted(committed_delta - allowed_delta))
            )
    if git("rev-parse", "origin/develop") != head:
        raise RuntimeError("local HEAD and origin/develop must match")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes present")
    committed_test_blob = git("rev-parse", "HEAD:" + R1R1_TEST)
    if committed_test_blob not in {R1R1_SOURCE_BLOB, R1R1_COMMITTED_BLOB}:
        raise RuntimeError("historical R3Z test baseline is not reviewed")
    test_file = ROOT / R1R1_TEST
    if hashlib.sha256(lf_text(test_file.read_bytes()).encode("utf-8")).hexdigest() != R1R1_EXPECTED:
        raise RuntimeError("R1R1 semantic test fix has not been installed or differs")
    before: dict[str, bytes] = {}
    after: dict[str, bytes] = {}
    for relative, blob in DOC_BLOBS.items():
        if git("rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("reviewed GitHub document blob changed: " + relative)
        source = (ROOT / relative).read_bytes()
        before[relative] = source
        committed = subprocess.run(["git", "show", "HEAD:" + relative],
                                   cwd=ROOT, capture_output=True, check=True).stdout
        if lf_text(source) == lf_text(committed):
            # A clean or platform-line-ending-only worktree preserves its
            # exact existing bytes; never normalize historical document text.
            after[relative] = updated_document(relative, source)
        else:
            expected = updated_document(relative, committed)
            if lf_text(source) != lf_text(expected):
                raise RuntimeError("unreviewed document worktree content: " + relative)
            # Already installed and fully reviewed: keep local historical
            # formatting rather than reconstituting the committed source.
            after[relative] = source
    tracked = {p for p in git("diff", "--name-only", "HEAD", "--").splitlines() if p}
    unexpected = tracked - {R1R1_TEST, *DOC_BLOBS}
    if unexpected:
        raise RuntimeError("unexpected tracked changes: " + ", ".join(sorted(unexpected)))
    if committed_test_blob == R1R1_SOURCE_BLOB and R1R1_TEST not in tracked:
        raise RuntimeError("R1R1 reviewed test change must remain in worktree")
    for relative in DOC_BLOBS:
        if relative in tracked and before[relative] != after[relative]:
            raise RuntimeError("pre-existing unreviewed document change: " + relative)
    missing = [p for p in FOCUSED if not (ROOT / p).is_file()]
    if missing:
        raise RuntimeError("missing focused test files: " + ", ".join(missing))
    return before, after, tracked
```

## test_document_writer.py の import 全文

```python
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
```

## `test_guarded_full_document_end_to_end_on_local_fixture()` テスト全文

```python
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
        elif relative == "docs/design.md":
            source = ("# 既存設計\r\r\n\r\r\n"
                      "既存の行。\r\n" + relative + "\n").encode("utf-8")
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
```

## `test_crcrlf_and_mixed_endings_preserve_exact_historical_bytes()` テスト全文

```python
def test_crcrlf_and_mixed_endings_preserve_exact_historical_bytes():
    from phase171_closeout_r2_documentation_full_output.update_docs import lf_text
    historical = (
        "# 設計記録\r\r\n\r\r\n"
        "過去の説明。\r\n別の説明。\n"
        "最後の段落。\r\n"
    ).encode("utf-8")
    revised = updated_document("docs/design.md", historical)
    assert revised.startswith(historical)
    assert revised != historical
    assert b"\r\r\n" in revised
    assert lf_text(revised).startswith(lf_text(historical))
    assert "Phase 171" in lf_text(revised)
```

## `test_many_crcrlf_in_historical_design_is_preserved()` テスト全文

```python
def test_many_crcrlf_in_historical_design_is_preserved():
    historical = ("過去の設計。\r\r\n" * 3401).encode("utf-8")
    revised = updated_document("docs/design.md", historical)
    assert revised.startswith(historical)
    assert revised[:len(historical)] == historical
    assert revised.count(b"\r\r\n") >= 3401
```

## `test_mixed_line_endings_and_bom_preserved_byte_for_byte()` テスト全文

```python
def test_mixed_line_endings_and_bom_preserved_byte_for_byte():
    historical = b"\xef\xbb\xbf" + (
        "# 証明記録\r\r\n旧段落。\r\n注記。\n"
    ).encode("utf-8")
    revised = updated_document("docs/proof_records.md", historical)
    assert revised.startswith(historical)
    assert revised[:len(historical)] == historical
```

## `test_bare_cr_still_refused()` テスト全文

```python
def test_bare_cr_still_refused():
    from phase171_closeout_r2_documentation_full_output.update_docs import lf_text
    with pytest.raises(ValueError, match="unknown line endings"):
        lf_text(b"text\rother")
```

## `test_crcrlf_normalizes_for_content_comparison()` テスト全文

```python
def test_crcrlf_normalizes_for_content_comparison():
    from phase171_closeout_r2_documentation_full_output.update_docs import lf_text
    source = b"A\r\r\nB\r\nC\n"
    committed = b"A\nB\nC\n"
    assert lf_text(source) == lf_text(committed)
```

## インストーラーと追加テスト

新規 `install.py` と `tests/test_install.py` は各ファイル全体を同梱。追加位置は新規ディレクトリ `phase171_closeout_r2r3_mixed_line_ending_fix/` 配下。
