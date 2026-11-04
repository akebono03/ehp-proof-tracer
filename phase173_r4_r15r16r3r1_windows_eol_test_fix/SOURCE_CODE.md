# R15R16R3R1 – 新規コードとテストの全文

## `install.py`

```python
"""R15R16R3R1: install one reviewed CRLF-sensitive test correction only."""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RELATIVE = Path("phase173_r4_r15r16r3_staged_guard_fix/tests/test_staged_guard.py")
TARGET = ROOT / RELATIVE
BASELINE = PACKAGE / "baseline_test_staged_guard.py.txt"
CORRECTED = PACKAGE / "test_staged_guard.py"
REVIEWED_HEAD = "92f967c079f4a66e19a598e0acc54b742f11df9c"
BASELINE_HASH = "31274cba1a86f3a695cb9f510c2c0de5bc647393a3bdc203911ac74be2438bb5"
CORRECTED_HASH = "8878fd8fd8990e902a8289eeaebabc5077df79cc8110ce44ea08f47fb0e5eebd"


def normalized(contents: bytes) -> bytes:
    return contents.replace(b"\r\n", b"\n")


def git(*arguments: str, binary: bool = False):
    response = subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True,
        check=False, **({} if binary else {"text": True, "encoding": "utf-8", "errors": "replace"}),
    )
    if response.returncode != 0:
        raise RuntimeError("git command failed: " + " ".join(arguments))
    return response.stdout if binary else response.stdout.strip()


def guard() -> str:
    if not TARGET.is_file():
        raise RuntimeError("existing R15R16R3 regression test is missing")
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or head != remote:
        raise RuntimeError("develop local/remote HEAD mismatch")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if ancestry.returncode != 0:
        raise RuntimeError("HEAD is not descended from reviewed R15R16")
    before = BASELINE.read_bytes()
    after = CORRECTED.read_bytes()
    if sha256(before).hexdigest() != BASELINE_HASH:
        raise RuntimeError("packaged baseline test content changed")
    if sha256(after).hexdigest() != CORRECTED_HASH:
        raise RuntimeError("packaged corrected test content changed")
    present = normalized(TARGET.read_bytes())
    present_hash = sha256(present).hexdigest()
    if present_hash not in (BASELINE_HASH, CORRECTED_HASH):
        raise RuntimeError("local regression test was edited; refusing to overwrite")
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    if RELATIVE.as_posix() in staged:
        indexed = normalized(git("show", ":" + RELATIVE.as_posix(), binary=True))
        indexed_hash = sha256(indexed).hexdigest()
        if indexed_hash not in (BASELINE_HASH, CORRECTED_HASH):
            raise RuntimeError("staged test content differs from reviewed test")
        if present_hash == BASELINE_HASH and indexed_hash != BASELINE_HASH:
            raise RuntimeError("staged test differs from pre-install working tree")
    print("R15R16R3R1_LOCAL_HEAD=" + head, flush=True)
    print("R15R16R3R1_INDEX_MODIFIED=False", flush=True)
    print("R15R16R3R1_SOURCE_GUARD=PASS", flush=True)
    return "corrected" if present_hash == CORRECTED_HASH else "baseline"


def project(template: bytes, original: bytes) -> bytes:
    if b"\r\n" in original:
        return normalized(template).replace(b"\n", b"\r\n")
    return normalized(template)


def install() -> None:
    state = guard()
    if state == "corrected":
        print("R15R16R3R1_ALREADY_INSTALLED=True", flush=True)
        return
    source = TARGET.read_bytes()
    TARGET.write_bytes(project(CORRECTED.read_bytes(), source))
    print("R15R16R3R1_TEST_CORRECTED=True", flush=True)
    print("R15R16R3R1_PRODUCTION_EDIT=NONE", flush=True)


def restore() -> None:
    state = guard()
    if state == "baseline":
        print("R15R16R3R1_ALREADY_RESTORED=True", flush=True)
        return
    source = TARGET.read_bytes()
    TARGET.write_bytes(project(BASELINE.read_bytes(), source))
    print("R15R16R3R1_TEST_RESTORED=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    choices = parser.add_mutually_exclusive_group(required=True)
    choices.add_argument("--dry-run", action="store_true")
    choices.add_argument("--install", action="store_true")
    choices.add_argument("--restore", action="store_true")
    options = parser.parse_args()
    try:
        if options.dry_run:
            state = guard()
            print("R15R16R3R1_EXISTING_TEST_STATE=" + state, flush=True)
            print("R15R16R3R1_DRY_RUN=PASS", flush=True)
        elif options.install:
            install()
        else:
            restore()
        return 0
    except (RuntimeError, OSError, UnicodeError) as exc:
        print("R15R16R3R1_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 Git fetch failed' }

    python -m phase173_r4_r15r16r3r1_windows_eol_test_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 source guard failed' }

    python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r16r3r1_windows_eol_test_fix/test_staged_guard.py `
      phase173_r4_r15r16r3r1_windows_eol_test_fix/tests/test_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 corrected test preview failed' }

    if ($DryRun) {
        Write-Output 'R15R16R3R1_DRY_RUN=PASS'
        Write-Output 'R15R16R3R1_PRODUCTION_EDIT=NONE'
        Write-Output 'R15R16R3R1_FULL_PYTEST_RUN=False'
        exit 0
    }

    python -m phase173_r4_r15r16r3r1_windows_eol_test_fix.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 test correction failed' }
    try {
        powershell -NoProfile -ExecutionPolicy Bypass `
          -File '.\phase173_r4_r15r16r3_staged_guard_fix\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 corrected original DryRun failed' }
        powershell -NoProfile -ExecutionPolicy Bypass `
          -File '.\phase173_r4_r15r16r3_staged_guard_fix\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 focused integration failed' }
        Write-Output 'R15R16R3R1_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R16R3R1_FULL_PYTEST_RUN=False'
        Write-Output 'R15R16R3R1_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r16r3r1_windows_eol_test_fix.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3R1 test rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
```

## `tests/test_contract.py`

```python
"""Pure validation that only the platform-specific byte expectation changes."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import subprocess

from phase173_r4_r15r16r3r1_windows_eol_test_fix import install


def test_corrected_file_replaces_exactly_one_assertion() -> None:
    before = install.BASELINE.read_text(encoding="utf-8")
    after = install.CORRECTED.read_text(encoding="utf-8")
    old = '    assert target.read_bytes() == original + b"# tested patch\\n"\n'
    new = ('    expected_eol = b"\\r\\n" if b"\\r\\n" in original else b"\\n"\n'
           '    assert target.read_bytes() == original + b"# tested patch" + expected_eol\n')
    assert before.count(old) == 1
    assert after == before.replace(old, new)
    assert sha256(before.encode("utf-8")).hexdigest() == install.BASELINE_HASH
    assert sha256(after.encode("utf-8")).hexdigest() == install.CORRECTED_HASH


def test_projection_preserves_existing_newline_style() -> None:
    replacement = b"one\ntwo\n"
    assert install.project(replacement, b"first\n") == replacement
    assert install.project(replacement, b"first\r\n") == b"one\r\ntwo\r\n"


def test_corrected_test_is_python_syntax_valid() -> None:
    source = install.CORRECTED.read_text(encoding="utf-8")
    compile(source, str(Path(install.CORRECTED)), "exec")


def test_guarded_install_and_restore_preserve_git_index(tmp_path, monkeypatch) -> None:
    root = tmp_path / "repo"
    root.mkdir()

    def git(*arguments: str) -> str:
        proc = subprocess.run(
            ["git", *arguments], cwd=root, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return proc.stdout.strip()

    git("init", "-q", "-b", "develop")
    git("config", "user.name", "Test Runner")
    git("config", "user.email", "test@example.org")
    target = root / install.RELATIVE
    target.parent.mkdir(parents=True)
    target.write_bytes(install.BASELINE.read_bytes())
    another = root / "other.txt"
    another.write_text("unchanged\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-qm", "reviewed baseline")
    head = git("rev-parse", "HEAD")
    git("update-ref", "refs/remotes/origin/develop", head)
    another.write_text("staged user content\n", encoding="utf-8")
    git("add", "other.txt")
    index_before = git("write-tree")

    monkeypatch.setattr(install, "ROOT", root)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "REVIEWED_HEAD", head)
    assert install.guard() == "baseline"
    install.install()
    assert target.read_bytes() == install.CORRECTED.read_bytes()
    assert git("write-tree") == index_before
    assert another.read_text(encoding="utf-8") == "staged user content\n"
    install.restore()
    assert target.read_bytes() == install.BASELINE.read_bytes()
    assert git("write-tree") == index_before


def test_staged_test_divergence_is_rejected(tmp_path, monkeypatch) -> None:
    root = tmp_path / "repo"
    root.mkdir()

    def git(*arguments: str) -> str:
        proc = subprocess.run(
            ["git", *arguments], cwd=root, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return proc.stdout.strip()

    git("init", "-q", "-b", "develop")
    git("config", "user.name", "Test Runner")
    git("config", "user.email", "test@example.org")
    target = root / install.RELATIVE
    target.parent.mkdir(parents=True)
    target.write_bytes(install.BASELINE.read_bytes())
    git("add", ".")
    git("commit", "-qm", "reviewed baseline")
    head = git("rev-parse", "HEAD")
    git("update-ref", "refs/remotes/origin/develop", head)
    target.write_bytes(install.CORRECTED.read_bytes())
    git("add", install.RELATIVE.as_posix())
    target.write_bytes(install.BASELINE.read_bytes())
    staged_before = git("write-tree")

    monkeypatch.setattr(install, "ROOT", root)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "REVIEWED_HEAD", head)
    try:
        install.guard()
    except RuntimeError as error:
        assert "staged test differs from pre-install working tree" in str(error)
    else:
        raise AssertionError("divergent staged test was accepted")
    assert git("write-tree") == staged_before
```

## `test_staged_guard.py`

```python
"""Index preservation and overlap validation in an isolated repository."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

from phase173_r4_r15r16r3_staged_guard_fix import install as installer


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, check=True,
        capture_output=True, text=True, encoding="utf-8",
    )
    return proc.stdout.strip()


def _setup_repo(tmp_path: Path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "develop")
    _git(root, "config", "user.email", "tester@example.org")
    _git(root, "config", "user.name", "Guard Test")
    for name in (installer.PROJECTION, installer.LAYOUT, installer.PREVIOUS_PATCH,
                 installer.PREVIOUS_TEST):
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fixed prior reviewed content\n", encoding="utf-8")
    (root / "other.txt").write_text("original\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "baseline")
    head = _git(root, "rev-parse", "HEAD")
    (root / ".git" / "refs" / "remotes" / "origin").mkdir(parents=True)
    _git(root, "update-ref", "refs/remotes/origin/develop", head)
    monkeypatch.setattr(installer, "ROOT", root)
    monkeypatch.setattr(installer, "REVIEWED_HEAD", head)
    monkeypatch.setattr(installer, "REVIEWED_BLOBS", {
        name: _git(root, "rev-parse", "HEAD:" + name)
        for name in (installer.PROJECTION, installer.LAYOUT)
    })
    monkeypatch.setattr(installer, "PREVIOUS_PATCH_SHA256", installer.sha256(
        (root / installer.PREVIOUS_PATCH).read_bytes()).hexdigest()
    )
    monkeypatch.setattr(installer, "PREVIOUS_TEST_SHA256", installer.sha256(
        (root / installer.PREVIOUS_TEST).read_bytes()).hexdigest()
    )
    monkeypatch.setattr(installer, "STATE", root / "state.json")
    monkeypatch.setattr(installer, "BACKUP", root / "backups")
    monkeypatch.setattr(
        installer, "expected_prior_local", lambda name, current: current,
    )
    return root


def test_unrelated_staged_edits_are_preserved(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    (root / "other.txt").write_text("user staged edit\n", encoding="utf-8")
    _git(root, "add", "other.txt")
    before = _git(root, "write-tree")
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert _git(root, "write-tree") == before
    assert (root / "other.txt").read_text() == "user staged edit\n"


def test_reviewed_staged_file_equal_worktree_is_allowed(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    # A real staged change is allowed only if the staged bytes and the
    # reviewed pre-install working tree bytes are exactly equal.
    target = root / installer.PROJECTION
    target.write_text("staged and reviewed prior state\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    before = _git(root, "write-tree")
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert _git(root, "write-tree") == before


def test_reviewed_staged_file_divergence_is_rejected(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("staged prior candidate\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    target.write_text("fixed prior reviewed content\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="staged reviewed file differs"):
        installer.source_guard()


def test_stage_safe_restore_reads_original_backup(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("newly staged reviewed change\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    target.write_text("installed patch output\n", encoding="utf-8")
    backup = root / "backups"
    backup.mkdir()
    (backup / "source_0.backup").write_bytes(b"newly staged reviewed change\n")
    state = {"files": {installer.PROJECTION: {
        "backup": "source_0.backup", "original_sha256": installer.sha256(
            b"newly staged reviewed change\n").hexdigest(),
    }}}
    installer.STATE.write_text(json.dumps(state), encoding="utf-8")
    # Here source_guard must skip the worktree equality test for staged
    # patched files, while proving the staged index is still the backup.
    monkeypatch.setattr(installer, "expected_prior_local", lambda name, current: current)
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")


def test_install_and_restore_preserve_staged_index(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("VALUE = 1\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    (root / "other.txt").write_text("user work kept in index\n", encoding="utf-8")
    _git(root, "add", "other.txt")
    index_before = _git(root, "write-tree")
    original = target.read_bytes()
    monkeypatch.setattr(installer, "TRANSFORMERS", {
        installer.PROJECTION: lambda source: source + "# tested patch\n",
    })

    installer.install()
    expected_eol = b"\r\n" if b"\r\n" in original else b"\n"
    assert target.read_bytes() == original + b"# tested patch" + expected_eol
    assert _git(root, "write-tree") == index_before
    assert _git(root, "show", ":" + installer.PROJECTION) == "VALUE = 1"
    assert (root / "other.txt").read_text() == "user work kept in index\n"

    # Re-running preflight is allowed even though the staged index keeps the
    # reviewed R15R16 bytes and the worktree contains the installed patch.
    installer.preflight()
    assert _git(root, "write-tree") == index_before

    installer.restore()
    assert target.read_bytes() == original
    assert _git(root, "write-tree") == index_before
    assert not installer.STATE.exists()


def test_windows_crlf_staged_blob_is_semantically_identical(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    _git(root, "config", "core.autocrlf", "true")
    target = root / installer.PROJECTION
    target.write_bytes(b"VALUE = 2\r\n")
    _git(root, "add", installer.PROJECTION)
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert target.read_bytes() == b"VALUE = 2\r\n"
```

## `baseline_test_staged_guard.py.txt`

```python
"""Index preservation and overlap validation in an isolated repository."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

from phase173_r4_r15r16r3_staged_guard_fix import install as installer


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, check=True,
        capture_output=True, text=True, encoding="utf-8",
    )
    return proc.stdout.strip()


def _setup_repo(tmp_path: Path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "develop")
    _git(root, "config", "user.email", "tester@example.org")
    _git(root, "config", "user.name", "Guard Test")
    for name in (installer.PROJECTION, installer.LAYOUT, installer.PREVIOUS_PATCH,
                 installer.PREVIOUS_TEST):
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fixed prior reviewed content\n", encoding="utf-8")
    (root / "other.txt").write_text("original\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "baseline")
    head = _git(root, "rev-parse", "HEAD")
    (root / ".git" / "refs" / "remotes" / "origin").mkdir(parents=True)
    _git(root, "update-ref", "refs/remotes/origin/develop", head)
    monkeypatch.setattr(installer, "ROOT", root)
    monkeypatch.setattr(installer, "REVIEWED_HEAD", head)
    monkeypatch.setattr(installer, "REVIEWED_BLOBS", {
        name: _git(root, "rev-parse", "HEAD:" + name)
        for name in (installer.PROJECTION, installer.LAYOUT)
    })
    monkeypatch.setattr(installer, "PREVIOUS_PATCH_SHA256", installer.sha256(
        (root / installer.PREVIOUS_PATCH).read_bytes()).hexdigest()
    )
    monkeypatch.setattr(installer, "PREVIOUS_TEST_SHA256", installer.sha256(
        (root / installer.PREVIOUS_TEST).read_bytes()).hexdigest()
    )
    monkeypatch.setattr(installer, "STATE", root / "state.json")
    monkeypatch.setattr(installer, "BACKUP", root / "backups")
    monkeypatch.setattr(
        installer, "expected_prior_local", lambda name, current: current,
    )
    return root


def test_unrelated_staged_edits_are_preserved(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    (root / "other.txt").write_text("user staged edit\n", encoding="utf-8")
    _git(root, "add", "other.txt")
    before = _git(root, "write-tree")
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert _git(root, "write-tree") == before
    assert (root / "other.txt").read_text() == "user staged edit\n"


def test_reviewed_staged_file_equal_worktree_is_allowed(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    # A real staged change is allowed only if the staged bytes and the
    # reviewed pre-install working tree bytes are exactly equal.
    target = root / installer.PROJECTION
    target.write_text("staged and reviewed prior state\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    before = _git(root, "write-tree")
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert _git(root, "write-tree") == before


def test_reviewed_staged_file_divergence_is_rejected(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("staged prior candidate\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    target.write_text("fixed prior reviewed content\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="staged reviewed file differs"):
        installer.source_guard()


def test_stage_safe_restore_reads_original_backup(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("newly staged reviewed change\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    target.write_text("installed patch output\n", encoding="utf-8")
    backup = root / "backups"
    backup.mkdir()
    (backup / "source_0.backup").write_bytes(b"newly staged reviewed change\n")
    state = {"files": {installer.PROJECTION: {
        "backup": "source_0.backup", "original_sha256": installer.sha256(
            b"newly staged reviewed change\n").hexdigest(),
    }}}
    installer.STATE.write_text(json.dumps(state), encoding="utf-8")
    # Here source_guard must skip the worktree equality test for staged
    # patched files, while proving the staged index is still the backup.
    monkeypatch.setattr(installer, "expected_prior_local", lambda name, current: current)
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")


def test_install_and_restore_preserve_staged_index(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("VALUE = 1\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    (root / "other.txt").write_text("user work kept in index\n", encoding="utf-8")
    _git(root, "add", "other.txt")
    index_before = _git(root, "write-tree")
    original = target.read_bytes()
    monkeypatch.setattr(installer, "TRANSFORMERS", {
        installer.PROJECTION: lambda source: source + "# tested patch\n",
    })

    installer.install()
    assert target.read_bytes() == original + b"# tested patch\n"
    assert _git(root, "write-tree") == index_before
    assert _git(root, "show", ":" + installer.PROJECTION) == "VALUE = 1"
    assert (root / "other.txt").read_text() == "user work kept in index\n"

    # Re-running preflight is allowed even though the staged index keeps the
    # reviewed R15R16 bytes and the worktree contains the installed patch.
    installer.preflight()
    assert _git(root, "write-tree") == index_before

    installer.restore()
    assert target.read_bytes() == original
    assert _git(root, "write-tree") == index_before
    assert not installer.STATE.exists()


def test_windows_crlf_staged_blob_is_semantically_identical(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    _git(root, "config", "core.autocrlf", "true")
    target = root / installer.PROJECTION
    target.write_bytes(b"VALUE = 2\r\n")
    _git(root, "add", installer.PROJECTION)
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert target.read_bytes() == b"VALUE = 2\r\n"
```

