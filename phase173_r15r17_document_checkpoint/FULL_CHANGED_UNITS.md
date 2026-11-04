# Phase 173 R15R17 documentation checkpoint — full changed units

## Implementation

All implementation files are newly added. No existing Python class/function/import is modified.

### New module imports (complete)

```python
"""Phase 173 R15R17 documentation checkpoint: full-file generation with strict guards.

Only verified R15R17 results are recorded. Browser visualization and phase-end
full pytest remain pending; existing historical text is preserved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


REVIEWED_BASE = "80e51d4c22f80e597e48a2f899eecac8ded8595d"
DOCUMENT_BLOBS = {
    "README.md": "1dac05e0f7310771009d307d8f535c6de3632a45",
```

### New function definitions (complete)
#### `docs_builder.py::apply_document_update`

```python
def apply_document_update(path: str, original: bytes) -> bytes:
    """Generate the complete Markdown file, preserving every historical byte."""
    if path not in DOCUMENT_BLOBS:
        raise ValueError("unreviewed document path")
    marker = MARKER.encode("utf-8")
    if marker in original:
        raise ValueError("checkpoint already applied or a duplicate marker exists")
    if path == "README.md":
        anchor = b"<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->"
        if original.count(anchor) != 1:
            raise ValueError("unreviewed README anchor")
        historical_title = b"## Current status \xe2\x80\x94 Phase 172 closed (2026-10-31)"
        if original.count(historical_title) != 1:
            raise ValueError("unreviewed Phase 172 heading")
        updated = original.replace(anchor, README_BLOCK.encode("utf-8") + anchor, 1)
        updated = updated.replace(
            historical_title,
            b"## Historical closeout \xe2\x80\x94 Phase 172 (2026-10-31)",
            1,
        )
    else:
        if not original.startswith(b"# EHP Proof Tracer"):
            raise ValueError(f"unreviewed document title: {path}")
        newline = b"\r\n" if original.endswith(b"\r\n") else b"\n"
        block = APPENDS[path].encode("utf-8").replace(b"\n", newline)
        updated = original + newline + block
    if updated.count(marker) != 1:
        raise ValueError("missing or duplicate checkpoint marker")
    if len(updated) <= len(original):
        raise ValueError("checkpoint must retain all historical content")
    return updated
```

#### `docs_builder.py::git`

```python
def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    process = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if check and process.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {process.stderr.strip()}")
    return process
```

#### `docs_builder.py::verify_repository`

```python
def verify_repository(repo: Path) -> None:
    if git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() != "develop":
        raise RuntimeError("expected develop branch")
    actual_repo = Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if actual_repo != repo.resolve():
        raise RuntimeError("ZIP must be extracted at the repository root")
    for ref in ("HEAD", "origin/develop"):
        if git(repo, "merge-base", "--is-ancestor", REVIEWED_BASE, ref, check=False).returncode:
            raise RuntimeError(f"{ref} is not a descendant of the reviewed Phase 173 HEAD")
    if git(repo, "merge-base", "--is-ancestor", "HEAD", "origin/develop", check=False).returncode:
        raise RuntimeError("local HEAD diverged from origin/develop")
    for path, expected in DOCUMENT_BLOBS.items():
        if git(repo, "diff", "--quiet", "HEAD", "--", path, check=False).returncode:
            raise RuntimeError(f"local document has unreviewed changes: {path}")
        if git(repo, "diff", "--cached", "--quiet", "--", path, check=False).returncode:
            raise RuntimeError(f"staged document has unreviewed changes: {path}")
        actual = git(repo, "rev-parse", f"HEAD:{path}").stdout.strip()
        if actual != expected:
            raise RuntimeError(f"document content changed on GitHub, needs rereview: {path}")
        if not (repo / path).is_file():
            raise RuntimeError(f"missing tracked document: {path}")
```

#### `docs_builder.py::sha256`

```python
def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
```

#### `docs_builder.py::atomic_write`

```python
def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".phase173_doc_", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        if path.exists():
            os.chmod(temporary, path.stat().st_mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)
```

#### `docs_builder.py::generate_files`

```python
def generate_files(repo: Path, package: Path, apply: bool) -> None:
    """Write all five full-file previews; on apply, replace verified tracked docs."""
    verify_repository(repo)
    preview_dir = package / "full_documents"
    preview_dir.mkdir(parents=True, exist_ok=True)
    documents = {}
    originals = {}
    for path in DOCUMENT_BLOBS:
        original = (repo / path).read_bytes()
        generated = apply_document_update(path, original)
        originals[path] = original
        documents[path] = generated
        atomic_write(preview_dir / path, generated)
        print(f"PHASE173_DOC_FULL_FILE={path} ORIGINAL_BYTES={len(original)} COMPLETE_BYTES={len(generated)}")
    status_before = git(repo, "diff", "--cached", "--name-status").stdout
    if apply:
        backup_dir = package / "original_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for path, content in originals.items():
            atomic_write(backup_dir / path, content)
        try:
            for path, content in documents.items():
                atomic_write(repo / path, content)
            for path, content in documents.items():
                if (repo / path).read_bytes() != content:
                    raise RuntimeError(f"document post-write mismatch: {path}")
        except BaseException:
            for path, content in originals.items():
                atomic_write(repo / path, content)
            raise
        (package / "installed_state.json").write_text(json.dumps({
            "reviewed_base": REVIEWED_BASE,
            "paths": {path: {"before": sha256(originals[path]),
                             "after": sha256(documents[path])}
                      for path in DOCUMENT_BLOBS},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if git(repo, "diff", "--cached", "--name-status").stdout != status_before:
        raise RuntimeError("Git index changed during documentation generation")
    print("PHASE173_R15R17_DOCS_GIT_INDEX_PRESERVED=PASS")
    print("PHASE173_R15R17_DOCS_FULL_OUTPUT=phase173_r15r17_document_checkpoint/full_documents/")
    print(f"PHASE173_R15R17_DOCS_{'INSTALL' if apply else 'DRY_RUN'}=PASS")
    if not apply:
        print("PHASE173_R15R17_DOCS_PRODUCTION_WRITES=NONE")
    print("PHASE173_R15R17_PHASE_END_FULL_PYTEST=NOT_RUN")
    print("PHASE173_R15R17_BROWSER_VISUAL_VERIFIED=UNCONFIRMED")
```

#### `docs_builder.py::main`

```python
def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 R15R17 full-file docs checkpoint")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    generate_files(args.repo.resolve(), args.package.resolve(), args.apply)
    return 0
```

## New test module (complete)

```python
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

```

## Full PowerShell script

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Not a Git repository' }
$ResolvedGitRoot = [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/')
$ResolvedRoot = [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/')
if ($ResolvedGitRoot -ine $ResolvedRoot) { throw 'Extract ZIP at repository root' }

Write-Output 'PHASE173_R15R17_DOCS_SCOPE=FIVE_FULL_MARKDOWN_FILES_ONLY'
Write-Output 'PHASE173_R15R17_DOCS_GIT_RESET_CLEAN_STAGE_COMMIT=NONE'
Write-Output 'PHASE173_R15R17_DOCS_FULL_PYTEST=False'

& git -C $Root -c core.quotepath=false fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'git fetch failed' }

Push-Location $Root
try {
    Write-Output '=== PHASE173 R15R17 DOCUMENT PATCH CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider '.\phase173_r15r17_document_checkpoint\tests\test_docs_builder.py'
    if ($LASTEXITCODE -ne 0) { throw 'Focused document test failed' }

    if ($DryRun) {
        & python -B -m phase173_r15r17_document_checkpoint.docs_builder --repo $Root --package $Package
    } else {
        & python -B -m phase173_r15r17_document_checkpoint.docs_builder --repo $Root --package $Package --apply
    }
    if ($LASTEXITCODE -ne 0) { throw 'Document generation failed' }
} finally {
    Pop-Location
}

```

## Full canonical documents

On `-DryRun` five complete post-change Markdown files are written into `full_documents/` using the current checkout as the exact input. The ZIP does not overwrite historical contents with abbreviated excerpts.
