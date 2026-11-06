# R17R2：実装コード・テスト全文

変更する実体は未追跡パッケージの `phase174_r3_r7_r17r1_historical_test_contract/audit.py` のみです。
既存の import は変更しません。下記は修正後の関数全体と新規関数全体です。

## 修正後の `audit.py` の import 全文（変更なし）

```python
"""R17R1: fail-closed source/contract gate for an obsolete historical test fixture."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from phase174_r3_r7_r17r1_historical_test_contract.patch import (
    TARGET as TEST_TARGET, EXPECTED_BLOB, original_matches, patched_bytes,
    normalized,
)
from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    TARGET as DISPLAY_TARGET, EXPECTED_BLOB as DISPLAY_BLOB,
    expected_patched_bytes, matches_git_blob,
)

```

## 追加関数 `expected_tracked_paths`

挿入位置：`git_bytes` 関数の後、`verify_source_and_state` 関数の直前。

```python
def expected_tracked_paths(*, applied: bool) -> tuple[str, ...]:
    """Use Git's repository-relative forward slash paths on every OS."""
    if type(applied) is not bool:
        raise TypeError("applied must be bool")
    if not applied:
        return ()
    return tuple(sorted((TEST_TARGET.as_posix(), DISPLAY_TARGET.as_posix())))
```

## 修正関数 `verify_source_and_state`（全文）

```python
def verify_source_and_state(*, applied: bool, root: Path = ROOT) -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract the package directly under the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError("Unreviewed GitHub/local HEAD; abort without checkout or reset")
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Unexpected staged files")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    expected_changed = expected_tracked_paths(applied=applied)
    if tuple(sorted(changed)) != expected_changed:
        raise RuntimeError("Unexpected tracked changes: " + str(changed))
    for relative, digest in R17_HELPERS.items():
        path = root / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError("R17 package differs from inspected original: " + relative)
    tracked_test = git_bytes("show", "HEAD:" + TEST_TARGET.as_posix(), root=root)
    if not original_matches(tracked_test):
        raise RuntimeError("Historical test Git blob no longer matches " + EXPECTED_BLOB)
    test_worktree = (root / TEST_TARGET).read_bytes()
    expected_test = patched_bytes(tracked_test) if applied else tracked_test
    if normalized(test_worktree)[0] != normalized(expected_test)[0]:
        raise RuntimeError("Historical test worktree changed unexpectedly")
    tracked_display = git_bytes("show", "HEAD:" + DISPLAY_TARGET.as_posix(), root=root)
    if not matches_git_blob(tracked_display, DISPLAY_BLOB):
        raise RuntimeError("Reviewed common formatter Git blob changed")
    local_display = (root / DISPLAY_TARGET).read_bytes()
    expected_display = expected_patched_bytes(tracked_display) if applied else tracked_display
    if normalized(local_display)[0] != normalized(expected_display)[0]:
        raise RuntimeError("Common formatter is not in the reviewed R17 state")
    return {"branch": "develop", "local_head": local, "remote_head": remote,
            "tracked_changes": list(changed), "source_guard": "PASS", "corrected_test_applied": applied,
            "source_hashes_checked": len(R17_HELPERS) + 2}
```

## 新規 `patch.py` のコード全文

```python
"""Guarded R17R1 source-guard correction; never change tracked proof code."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase174_r3_r7_r17r1_historical_test_contract/audit.py")
PRIOR_RUNNER = Path("phase174_r3_r7_r17r1_historical_test_contract/run.ps1")
EXPECTED_HEAD = "388f63797a6aba61418bb93e734b8ce5999dc7f6"
OLD_SHA256 = "8e06ed616290600ca8de431e5fe9c8f1662ee4795b413fb857f5c4a20fdd7d03"
RUNNER_SHA256 = "a483de03c09de729a36e6ec97afa302cdbc81d750f36a01a19169e8d2b2e16f7"
AUDITED_TRACKED = (
    "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
    "web_group_proof_common.py",
)
OLD_LINE = "    expected_changed = tuple(sorted((str(TEST_TARGET), str(DISPLAY_TARGET)))) if applied else ()\n"
NEW_LINE = "    expected_changed = expected_tracked_paths(applied=applied)\n"
INSERT_BEFORE = "def verify_source_and_state(*, applied: bool, root: Path = ROOT) -> dict[str, object]:\n"
NEW_HELPER = '''def expected_tracked_paths(*, applied: bool) -> tuple[str, ...]:
    """Use Git's repository-relative forward slash paths on every OS."""
    if type(applied) is not bool:
        raise TypeError("applied must be bool")
    if not applied:
        return ()
    return tuple(sorted((TEST_TARGET.as_posix(), DISPLAY_TARGET.as_posix())))


'''
BACKUP = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) /
          "EHPProofTracerAudit" / "phase174_r3_r7_r17r2" / "r17r1_audit.original.py")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform(source: str) -> str:
    """Change only the OS-sensitive worktree-file comparison."""
    if source.count(OLD_LINE) != 1 or source.count(INSERT_BEFORE) != 1:
        raise RuntimeError("Reviewed R17R1 guard anchor missing or duplicated")
    if "def expected_tracked_paths(" in source:
        raise RuntimeError("R17R2 guard already installed")
    transformed = source.replace(OLD_LINE, NEW_LINE, 1)
    transformed = transformed.replace(INSERT_BEFORE, NEW_HELPER + INSERT_BEFORE, 1)
    if transformed.count(NEW_LINE) != 1:
        raise RuntimeError("R17R2 guard did not install exactly once")
    compile(transformed, str(TARGET), "exec")
    return transformed


def normalized(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM in R17R1 audit source")
    text = data.decode("utf-8")
    if b"\r\n" in data:
        if b"\n" in data.replace(b"\r\n", b""):
            raise RuntimeError("Mixed EOLs are not accepted")
        text = text.replace("\r\n", "\n")
    elif "\r" in text:
        raise RuntimeError("Bare carriage return in source")
    return text


def patched_bytes(original: bytes) -> bytes:
    content = transform(normalized(original))
    if b"\r\n" in original:
        return content.replace("\n", "\r\n").encode("utf-8")
    return content.encode("utf-8")


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(("git",) + args, cwd=root, check=True,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def verify_git_and_package(*, applied: bool = False, root: Path = ROOT) -> None:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R17R2 directly into the repo root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Only the reviewed develop branch is permitted")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError("Local and origin/develop must match the reviewed R17 HEAD")
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged changes require review")
    modified = tuple(sorted(git("diff", "--name-only", root=root).splitlines()))
    expected = AUDITED_TRACKED if applied else ()
    if modified != expected:
        raise RuntimeError("Unexpected tracked changes during R17R2: " + str(modified))
    runner = root / PRIOR_RUNNER
    if not runner.is_file() or sha256(runner.read_bytes()) != RUNNER_SHA256:
        raise RuntimeError("The previously reviewed R17R1 runner has changed")
    if not (root / "phase174_r3_r7_r17_typed_map_open_goal" / "run.ps1").is_file():
        raise RuntimeError("Previously extracted R17 package is required")


def checked_state(*, root: Path = ROOT) -> str:
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("Previously extracted R17R1 audit.py is required")
    raw = path.read_bytes()
    old = sha256(raw) == OLD_SHA256
    new = False
    if not old:
        try:
            source = normalized(raw)
            new = (NEW_LINE in source and NEW_HELPER in source
                   and OLD_LINE not in source)
            if new and BACKUP.is_file():
                original = BACKUP.read_bytes()
                new = sha256(original) == OLD_SHA256 and raw == patched_bytes(original)
        except (RuntimeError, UnicodeError):
            new = False
    if old:
        return "REVIEWED_ORIGINAL"
    if new:
        return "EXACT_REVIEWED_PATCH"
    raise RuntimeError("The R17R1 audit script does not match the reviewed state")


def apply(*, root: Path = ROOT) -> str:
    verify_git_and_package(root=root)
    status = checked_state(root=root)
    if status == "EXACT_REVIEWED_PATCH":
        return "ALREADY_APPLIED"
    path = root / TARGET
    original = path.read_bytes()
    transformed = patched_bytes(original)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != original:
        raise RuntimeError("Existing R17R2 backup differs; manual review required")
    BACKUP.write_bytes(original)
    temporary = path.with_suffix(".r17r2.tmp")
    if temporary.exists():
        raise RuntimeError("Temporary R17R2 file already exists")
    try:
        temporary.write_bytes(transformed)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    if checked_state(root=root) != "EXACT_REVIEWED_PATCH":
        raise RuntimeError("R17R2 patch verification failed")
    return "APPLIED"


def rollback(*, root: Path = ROOT) -> str:
    state = checked_state(root=root)
    if state == "REVIEWED_ORIGINAL":
        return "ALREADY_ORIGINAL"
    original = BACKUP.read_bytes()
    if sha256(original) != OLD_SHA256:
        raise RuntimeError("Stored R17R1 script backup is not the reviewed original")
    (root / TARGET).write_bytes(original)
    return "RESTORED"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    if args.rollback:
        value = rollback()
    else:
        verify_git_and_package(applied=args.verify)
        if args.dry_run:
            status = checked_state()
            if status != "REVIEWED_ORIGINAL":
                raise RuntimeError("DryRun expects the original R17R1 audit script")
            predicted = patched_bytes((ROOT / TARGET).read_bytes())
            value = "PASS_PREFLIGHT_SHA=" + sha256(predicted)
        elif args.apply:
            value = apply()
        else:
            value = checked_state()
            if value != "EXACT_REVIEWED_PATCH":
                raise RuntimeError("R17R2 guard not yet applied")
    print("PHASE174_R3R7R17R2_GUARD=" + value)
    print("PHASE174_R3R7R17R2_TARGET=" + TARGET.as_posix())
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 `run.ps1` のコード全文

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalPythonPath = $env:PYTHONPATH
$OriginalNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$GuardAppliedByThisRun = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R17R2 git fetch failed' }

    & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R17R2 guarded preflight failed' }

    Write-Output 'PHASE174_R3R7R17R2_PYTEST_GROUP=PATH_CONTRACT'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
        '.\phase174_r3_r7_r17r2_windows_git_path_guard_fix\tests\test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R17R2 focused path contract failed' }

    $PriorRunner = '.\phase174_r3_r7_r17r1_historical_test_contract\run.ps1'
    if (-not (Test-Path -LiteralPath $PriorRunner)) {
        throw 'Previously extracted R17R1 run.ps1 is missing'
    }

    if ($DryRun) {
        & powershell -NoProfile -ExecutionPolicy Bypass -File $PriorRunner -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R17R1 original DryRun failed' }
        Write-Output 'PHASE174_R3R7R17R2_GATE=PASS_PREFLIGHT_WINDOWS_PATH_CORRECTION'
    }
    else {
        $GuardAppliedByThisRun = $true
        & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R17R2 guarded audit correction failed' }

        Write-Output 'PHASE174_R3R7R17R2_PYTEST_GROUP=LIVE_GUARD'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r17r2_windows_git_path_guard_fix\tests\test_live_guard.py'
        if ($LASTEXITCODE -ne 0) { throw 'R17R2 live guard regression failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass -File $PriorRunner
        if ($LASTEXITCODE -ne 0) { throw 'Corrected R17R1 delegated execution failed' }

        & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'R17R2 guard verification failed' }
        Write-Output 'PHASE174_R3R7R17R2_GATE=PASS_WINDOWS_GIT_PATH_GUARD_R17R1_FINAL'
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_.ToString()
    if ($GuardAppliedByThisRun) {
        & python -B -m phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Warning 'R17R2 source-guard rollback needs manual review'
        }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $OriginalPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OriginalNoBytecode
    Pop-Location
}
```

## 新規限定テスト `test_patch.py` の import とテスト関数全文

```python
"""Pure focused regression tests: Git paths must be POSIX across Windows/Linux."""
from __future__ import annotations

import ast
import pytest

from phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch import (
    AUDITED_TRACKED, EXPECTED_HEAD, NEW_HELPER, NEW_LINE, OLD_LINE, patched_bytes,
    sha256, transform, normalized,
)


def original_fixture() -> str:
    return (
        "from pathlib import Path\n"
        "TEST_TARGET = Path('phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py')\n"
        "DISPLAY_TARGET = Path('web_group_proof_common.py')\n"
        "\n\n"
        "ROOT = Path('.')\n\n"
        "def verify_source_and_state(*, applied: bool, root: Path = ROOT) -> dict[str, object]:\n"
        + OLD_LINE
        + "    return expected_changed\n"
    )


def test_windows_git_slash_mismatch_is_repaired_without_broadening_guard() -> None:
    previous = original_fixture()
    corrected = transform(previous)
    ast.parse(corrected)
    assert OLD_LINE not in corrected
    assert corrected.count(NEW_LINE) == 1
    assert corrected.count(NEW_HELPER) == 1
    namespace: dict[str, object] = {}
    exec(compile(corrected, "fixture", "exec"), namespace)
    expected = (
        "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
        "web_group_proof_common.py",
    )
    assert namespace["verify_source_and_state"](applied=True) == expected
    assert namespace["verify_source_and_state"](applied=False) == ()
    assert namespace["verify_source_and_state"](applied=True) != expected + ("other.py",)


def test_expected_tracked_paths_requires_boolean_applied() -> None:
    corrected = transform(original_fixture())
    scope: dict[str, object] = {}
    exec(compile(corrected, "fixture", "exec"), scope)
    for invalid in (None, 1, "True", (), object()):
        with pytest.raises(TypeError):
            scope["expected_tracked_paths"](applied=invalid)


def test_patch_rejects_missing_repeated_and_previous_transformation() -> None:
    source = original_fixture()
    with pytest.raises(RuntimeError):
        transform(source.replace(OLD_LINE, ""))
    with pytest.raises(RuntimeError):
        transform(source + OLD_LINE)
    with pytest.raises(RuntimeError):
        transform(transform(source))


def test_patch_bytes_preserve_crlf_or_lf() -> None:
    source = original_fixture().encode("utf-8")
    lf = patched_bytes(source)
    crlf = patched_bytes(source.replace(b"\n", b"\r\n"))
    assert b"\r\n" not in lf
    assert b"\r\n" in crlf
    assert normalized(lf) == normalized(crlf)
    assert normalized(crlf).count("def expected_tracked_paths(") == 1


def test_mixed_eol_is_rejected_and_expected_head_is_pinned() -> None:
    source = original_fixture().encode("utf-8")
    with pytest.raises(RuntimeError):
        normalized(source.replace(b"\n", b"\r\n", 1))
    assert len(EXPECTED_HEAD) == 40
    assert len(sha256(source)) == 64


def test_expected_tracked_modifications_are_the_exact_two_reviewed_files() -> None:
    assert AUDITED_TRACKED == (
        "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
        "web_group_proof_common.py",
    )
```

## 新規統合テスト `test_live_guard.py` の import とテスト関数全文

```python
"""After applying, assert exact Git path names and unchanged proof semantics."""
from __future__ import annotations

from phase174_r3_r7_r17r1_historical_test_contract.audit import expected_tracked_paths
from phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch import checked_state


def test_live_r17r1_guard_recognizes_git_forward_slashes() -> None:
    assert checked_state() == "EXACT_REVIEWED_PATCH"
    assert expected_tracked_paths(applied=False) == ()
    assert expected_tracked_paths(applied=True) == (
        "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
        "web_group_proof_common.py",
    )
```
