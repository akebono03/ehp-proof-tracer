# Phase 174 R3-R7-R18R1：変更後のコード全文

## 変更ファイル・関数・追加位置

`phase174_r3_r7_r18_delta_image_surjectivity/audit.py`：新規定数 `R18_MERGED_HEAD` / `R18_AUDIT_PATH` は `REVIEWED_HEAD` の直後、新規関数 `matches_reviewed_checkout` は `matches_git_blob` の直後。既存関数 `checked_lineage`、`verify_git_and_sources` を全文置換。import 変更なし。

## 既存 audit.py：変更後の import 全文

```python
"""R18 source-first review of a noncircular Delta-surjectivity branch.

The common public search remains unchanged. An isolated GoalExpansion
records obligations, not a proof or a root completion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any
```

## 追加定数

```python
REVIEWED_HEAD = "4d59298949c14dc02d8bfb6ec28da4624ed980da"
R18_MERGED_HEAD = "7ecd12f28b5943b105ac6a953be69b44eae4a26e"
R18_AUDIT_PATH = "phase174_r3_r7_r18_delta_image_surjectivity/audit.py"
```

## 関数全文：`matches_reviewed_checkout`

```python
def matches_reviewed_checkout(data: bytes, expected: str, git_stored: bytes) -> bool:
    """Accept only the pinned Git blob or exact uniform EOL checkout variants.

    Git may store mixed LF/CRLF in a reviewed file. A clean checkout can
    preserve those exact bytes or convert all line endings consistently.
    No character other than CR or LF may differ from the pinned Git object.
    """
    if git_blob_sha(git_stored) != expected:
        return False
    normalized = git_stored.replace(b"\r\n", b"\n")
    return data in (
        git_stored,
        normalized,
        normalized.replace(b"\n", b"\r\n"),
    )
```

## 関数全文：`checked_lineage`

```python
def checked_lineage(local: str, remote: str, changes: tuple[str, ...],
                    committed: tuple[str, ...]) -> str:
    """Require an exactly reviewed R17 history and R18 handoff, if merged."""
    allowed_committed = set(HANDOFF_TRACKED)
    if (not set(HANDOFF_TRACKED).issubset(set(committed))
            or any(path not in allowed_committed and not path.startswith(
                ("phase174_r3_r7_r17_typed_map_open_goal/",
                 "phase174_r3_r7_r17r1_historical_test_contract/",
                 "phase174_r3_r7_r17r2_windows_git_path_guard_fix/"),
            ) for path in committed)):
        raise RuntimeError("Remote R17 merge lineage has unexpected files")
    if remote == REVIEWED_HEAD:
        if local == REVIEWED_HEAD and changes == ():
            return "R17_MERGED_CLEAN"
        if local == PRE_R17_HEAD and tuple(sorted(changes)) == HANDOFF_TRACKED:
            return "R17_PATCHES_UNCOMMITTED_MATCH_MERGED_REMOTE"
        raise RuntimeError("Unreviewed R17 worktree state: " + repr(changes))
    if remote != R18_MERGED_HEAD:
        raise RuntimeError("Unreviewed remote develop HEAD; no checkout/reset")
    if local == REVIEWED_HEAD and changes == ():
        return "R18_MERGED_REMOTE_R17_LOCAL_CLEAN"
    if local == R18_MERGED_HEAD and changes == ():
        return "R18_MERGED_CLEAN"
    if local == R18_MERGED_HEAD and changes == (R18_AUDIT_PATH,):
        return "R18_MERGED_REVIEWED_GUARD_FIX"
    raise RuntimeError("Unreviewed R18 worktree changes: " + repr(changes))
```

## 関数全文：`verify_git_and_sources`

```python
def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    repo = Path(git("rev-parse", "--show-toplevel", root=root)).resolve()
    if repo != root.resolve():
        raise RuntimeError("Extract the R18 folder directly under repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R18 requires develop branch")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged changes require separate audit")
    changes = tuple(git("diff", "--name-only", root=root).splitlines())
    git_bytes("merge-base", "--is-ancestor", PRE_R17_HEAD, REVIEWED_HEAD, root=root)
    commits = tuple(git("rev-list", PRE_R17_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines())
    if len(commits) != 1:
        raise RuntimeError("Expected one reviewed R17 merge commit")
    changed_in_review = tuple(git(
        "diff", "--name-only", PRE_R17_HEAD, REVIEWED_HEAD, root=root,
    ).splitlines())
    lineage = checked_lineage(local, remote, changes, changed_in_review)
    if remote == R18_MERGED_HEAD:
        git_bytes("merge-base", "--is-ancestor", REVIEWED_HEAD, R18_MERGED_HEAD, root=root)
        r18_commits = git("rev-list", REVIEWED_HEAD + ".." + R18_MERGED_HEAD, root=root).splitlines()
        r18_paths = git("diff", "--name-only", REVIEWED_HEAD, R18_MERGED_HEAD, root=root).splitlines()
        if (len(r18_commits) != 1 or not r18_paths
                or any(not p.startswith("phase174_r3_r7_r18_delta_image_surjectivity/")
                       for p in r18_paths)):
            raise RuntimeError("Unreviewed R18 merge lineage")
    for relative, blob in PINS.items():
        file = root / relative
        git_stored = git_bytes("show", "HEAD:" + relative, root=root)
        if (not file.is_file()
                or not matches_reviewed_checkout(file.read_bytes(), blob, git_stored)):
            raise RuntimeError("R18 Source Guard mismatch: " + relative)
    for relative in HANDOFF_TRACKED:
        reviewed = git_bytes("show", REVIEWED_HEAD + ":" + relative, root=root)
        if git_blob_sha(reviewed) != PINS[relative]:
            raise RuntimeError("Reviewed GitHub R17 target mismatch: " + relative)
    return {
        "local_head": local, "remote_head": remote,
        "lineage": lineage, "source_guard": "PASS",
        "pinned_files": len(PINS), "tracked_changes": list(changes),
    }
```

## 既存 audit.py の完全な置換用ファイル

同梱 `replacement_audit.py.txt` が import を含むファイル全文。SHA-256 と git lineage を検証後にのみ `patch.py` が適用する。

## 新規ファイル全文：`patch.py`

```python
"""Guarded, exact whole-file R18 audit correction; no production code edits."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path('phase174_r3_r7_r18_delta_image_surjectivity/audit.py')
REPLACEMENT = Path(__file__).resolve().parent / 'replacement_audit.py.txt'
BEFORE_SHA256 = 'e0e0c986762f76dc601b0cdf6c01d81eece696dc2bb5f593ca0fd2debf045c73'
AFTER_SHA256 = '7ff6ab7b4f4b7595c6e16216e8c3a8e1edf3845cc4dcfdb3165879e4c7f57aaa'
REVIEWED_R17_HEAD = '4d59298949c14dc02d8bfb6ec28da4624ed980da'
REVIEWED_R18_HEAD = '7ecd12f28b5943b105ac6a953be69b44eae4a26e'
R18_PACKAGE_PREFIX = 'phase174_r3_r7_r18_delta_image_surjectivity/'
R18_AUDIT = TARGET.as_posix()
SOURCE_FILES = (
    'phase174_r3_r7_r18_delta_image_surjectivity/rule.py',
    'phase174_r3_r7_r18_delta_image_surjectivity/run.ps1',
    'phase174_r3_r7_r18_delta_image_surjectivity/tests/test_audit.py',
    'phase174_r3_r7_r18_delta_image_surjectivity/tests/test_rule.py',
)
BACKUP = (
    Path(os.environ.get('LOCALAPPDATA', tempfile.gettempdir()))
    / 'EHPProofTracerAudit' / 'phase174_r3_r7_r18r1'
    / 'audit_original.py'
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ('git',) + args, cwd=root, check=True, text=True,
        capture_output=True, encoding='utf-8', errors='replace',
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ('git',) + args, cwd=root, check=True, capture_output=True,
    ).stdout


def exact_replacement() -> bytes:
    data = REPLACEMENT.read_bytes()
    if digest(data) != AFTER_SHA256:
        raise RuntimeError('Unreviewed R18R1 replacement content')
    compile(data.decode('utf-8'), R18_AUDIT, 'exec')
    return data


def source_state(root: Path = ROOT) -> str:
    data = (root / TARGET).read_bytes()
    value = digest(data)
    if value == BEFORE_SHA256:
        return 'ORIGINAL'
    if value == AFTER_SHA256 and data == exact_replacement():
        return 'PATCHED'
    raise RuntimeError('R18 audit.py does not match either reviewed source state')


def verify_host(*, patched: bool, root: Path = ROOT) -> dict[str, str]:
    if Path(git('rev-parse', '--show-toplevel', root=root)).resolve() != root.resolve():
        raise RuntimeError('Extract R18R1 under the repo root')
    if git('branch', '--show-current', root=root) != 'develop':
        raise RuntimeError('Expected develop branch')
    local = git('rev-parse', 'HEAD', root=root)
    remote = git('ls-remote', 'origin', 'refs/heads/develop', root=root).split()[0]
    if remote != REVIEWED_R18_HEAD or local not in (REVIEWED_R17_HEAD, REVIEWED_R18_HEAD):
        raise RuntimeError('Unreviewed local/remote HEAD; refuse automatic patch')
    if git('diff', '--cached', '--name-only', root=root):
        raise RuntimeError('Staged changes need separate review')
    changed = tuple(git('diff', '--name-only', root=root).splitlines())
    permitted = (R18_AUDIT,) if patched and local == REVIEWED_R18_HEAD else ()
    if changed != permitted:
        raise RuntimeError('Unexpected tracked changes: ' + repr(changed))
    git_bytes('merge-base', '--is-ancestor', REVIEWED_R17_HEAD, REVIEWED_R18_HEAD, root=root)
    commits = git('rev-list', REVIEWED_R17_HEAD + '..' + REVIEWED_R18_HEAD, root=root).splitlines()
    paths = git('diff', '--name-only', REVIEWED_R17_HEAD, REVIEWED_R18_HEAD, root=root).splitlines()
    if len(commits) != 1 or not paths or any(not p.startswith(R18_PACKAGE_PREFIX) for p in paths):
        raise RuntimeError('Unreviewed R18 merge contents')
    source = git_bytes('show', 'origin/develop:' + R18_AUDIT, root=root)
    if digest(source) != BEFORE_SHA256:
        raise RuntimeError('Remote reviewed R18 audit.py changed')
    if source_state(root=root) != ('PATCHED' if patched else 'ORIGINAL'):
        raise RuntimeError('R18 audit.py in unexpected state')
    for path in SOURCE_FILES:
        local_source = root / path
        if not local_source.is_file():
            raise RuntimeError('Missing R18 reviewed source: ' + path)
        committed = git_bytes('show', 'origin/develop:' + path, root=root)
        if local_source.read_bytes() != committed:
            raise RuntimeError('R18 reviewed package source mismatch: ' + path)
    exact_replacement()
    return {'local': local, 'remote': remote, 'state': source_state(root=root)}


def apply(root: Path = ROOT) -> str:
    state = source_state(root=root)
    verify_host(patched=state == 'PATCHED', root=root)
    if state == 'PATCHED':
        if not BACKUP.is_file() or digest(BACKUP.read_bytes()) != BEFORE_SHA256:
            raise RuntimeError('Missing reviewed R18R1 backup for an already applied patch')
        return 'ALREADY_APPLIED'
    before = (root / TARGET).read_bytes()
    updated = exact_replacement()
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != before:
        raise RuntimeError('Unexpected existing R18R1 backup')
    BACKUP.write_bytes(before)
    tmp = (root / TARGET).with_suffix('.r18r1.tmp')
    if tmp.exists():
        raise RuntimeError('Temporary patch file exists; inspect before retry')
    try:
        tmp.write_bytes(updated)
        os.replace(tmp, root / TARGET)
    finally:
        if tmp.exists():
            tmp.unlink()
    verify_host(patched=True, root=root)
    return 'APPLIED'


def rollback(root: Path = ROOT) -> str:
    if source_state(root=root) == 'ORIGINAL':
        return 'ALREADY_ORIGINAL'
    if not BACKUP.is_file():
        raise RuntimeError('Original R18 audit backup missing')
    original = BACKUP.read_bytes()
    if digest(original) != BEFORE_SHA256:
        raise RuntimeError('Stored backup does not match original source')
    (root / TARGET).write_bytes(original)
    return 'RESTORED'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--dry-run', action='store_true')
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--verify', action='store_true')
    mode.add_argument('--rollback', action='store_true')
    args = parser.parse_args()
    if args.rollback:
        outcome = rollback()
    elif args.apply:
        outcome = apply()
    else:
        state = source_state()
        verify_host(patched=state == 'PATCHED')
        if args.verify and state != 'PATCHED':
            raise RuntimeError('Expected applied R18R1 patch')
        outcome = 'PASS_PREFLIGHT_' + state if args.dry_run else 'PASS_VERIFIED_PATCH'
    print('PHASE174_R3R7R18R1_GUARD=' + outcome)
    print('PHASE174_R3R7R18R1_TARGET=' + R18_AUDIT)
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## 新規ファイル全文：`run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
$AppliedByThisRun = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R18R1 git fetch failed' }

    & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R18R1 reviewed Source Guard preflight failed' }

    Write-Output 'PHASE174_R3R7R18R1_PYTEST_GROUP=GUARD_CONTRACT'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
        '.\phase174_r3_r7_r18r1_git_mixed_eol_guard\tests\test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R18R1 guard contract pytest failed' }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R18R1_GATE=PASS_PREFLIGHT_MIXED_EOL_GUARD'
    }
    else {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R18R1 reviewed audit correction failed' }
        $AppliedByThisRun = $true

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R18 corrected DryRun failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'R18 corrected public audit failed' }

        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'R18R1 final source verification failed' }
        Write-Output 'PHASE174_R3R7R18R1_GATE=PASS_REVIEWED_GIT_MIXED_EOL_R18_PUBLIC'
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_
    if ($AppliedByThisRun) {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE174_R3R7R18R1_ROLLBACK=FAILED_MANUAL_REVIEW_REQUIRED'
        }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    Pop-Location
}
```

## 新規ファイル全文：`tests/test_patch.py`

```python
"""R18R1 mixed-EOL Git-object guard and reviewed lineage contracts."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r18r1_git_mixed_eol_guard.patch import (
    AFTER_SHA256,
    BEFORE_SHA256,
    REPLACEMENT,
    REVIEWED_R17_HEAD,
    REVIEWED_R18_HEAD,
    digest,
    exact_replacement,
)


def _reviewed_module():
    namespace = {'__name__': 'phase174_r3_r7_r18r1_test_target', '__file__': str(REPLACEMENT)}
    exec(compile(exact_replacement(), str(REPLACEMENT), 'exec'), namespace)
    return namespace


def _committed():
    return (
        'phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py',
        'web_group_proof_common.py',
        'phase174_r3_r7_r17_typed_map_open_goal/patch.py',
    )


def test_full_replacement_integrity_and_syntax() -> None:
    data = exact_replacement()
    assert digest(data) == AFTER_SHA256
    assert BEFORE_SHA256 != AFTER_SHA256
    ast.parse(data.decode('utf-8'))
    assert b'git reset' not in data


def test_exact_mixed_eol_blob_is_accepted() -> None:
    module = _reviewed_module()
    data = b'one\r\ntwo\nthree\r\n'
    expected = module['git_blob_sha'](data)
    assert module['matches_reviewed_checkout'](data, expected, data)
    assert not module['matches_git_blob'](data, expected)


def test_uniform_checkout_forms_accepted_only_from_pinned_blob() -> None:
    module = _reviewed_module()
    committed = b'one\r\ntwo\nthree\r\n'
    expected = module['git_blob_sha'](committed)
    assert module['matches_reviewed_checkout'](b'one\ntwo\nthree\n', expected, committed)
    assert module['matches_reviewed_checkout'](b'one\r\ntwo\r\nthree\r\n', expected, committed)


@pytest.mark.parametrize('file', (
    b'one\r\ntwo\nthree\n',
    b'one\ntwo\nthree corrupted\n',
    b'one\r\ntwo\nthree\r\n\n',
))
def test_changed_or_unreviewed_checkout_rejected(file: bytes) -> None:
    module = _reviewed_module()
    committed = b'one\r\ntwo\nthree\r\n'
    expected = module['git_blob_sha'](committed)
    assert not module['matches_reviewed_checkout'](file, expected, committed)


def test_wrong_stored_blob_pin_rejected() -> None:
    module = _reviewed_module()
    committed = b'one\r\ntwo\nthree\r\n'
    assert not module['matches_reviewed_checkout'](committed, 'a' * 40, committed)


def test_reviwed_original_lineage_supported() -> None:
    module = _reviewed_module()
    assert module['checked_lineage'](REVIEWED_R17_HEAD, REVIEWED_R17_HEAD, (), _committed()) == 'R17_MERGED_CLEAN'


def test_r18_merged_clean_and_own_audit_edit_supported() -> None:
    module = _reviewed_module()
    marker = 'phase174_r3_r7_r18_delta_image_surjectivity/audit.py'
    assert module['checked_lineage'](REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, (), _committed()) == 'R18_MERGED_CLEAN'
    assert module['checked_lineage'](REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, (marker,), _committed()) == 'R18_MERGED_REVIEWED_GUARD_FIX'
    assert module['checked_lineage'](REVIEWED_R17_HEAD, REVIEWED_R18_HEAD, (), _committed()) == 'R18_MERGED_REMOTE_R17_LOCAL_CLEAN'


@pytest.mark.parametrize('bad', (
    ('b' * 40, REVIEWED_R18_HEAD, ()),
    (REVIEWED_R18_HEAD, 'a' * 40, ()),
    (REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, ('proof.py',)),
    (REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, ('phase174_r3_r7_r18_delta_image_surjectivity/rule.py',)),
))
def test_unknown_lineages_fail_closed(bad) -> None:
    module = _reviewed_module()
    with pytest.raises(RuntimeError):
        module['checked_lineage'](bad[0], bad[1], bad[2], _committed())


def test_r18_unreviewed_old_committed_paths_rejected() -> None:
    module = _reviewed_module()
    with pytest.raises(RuntimeError, match='unexpected files'):
        module['checked_lineage'](REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, (), _committed() + ('proof.py',))


def test_no_production_search_or_rule_changes() -> None:
    data = exact_replacement().decode('utf-8')
    assert 'def inspect_live_frontier' in data
    assert 'production_provider_changed": False' in data
    assert 'new_group_given": 0' in data
```

## 限定テストと Gate

パッケージ契約テストと既存 R18 監査テストを実施し、現地の R18 `run.ps1` の限定 pytest を再実行する。

本実行期待 Gate：`PASS_REVIEWED_GIT_MIXED_EOL_R18_PUBLIC`。

Phase 境界：数学的な証明の完成や公開接続は行わない。全体 pytest は Phase 末に限定する。
