# Phase 172 R3R1R1：変更コード全文

## 変更対象

- `phase172_r3r1_hopf_chain_audit/audit.py`：定数1件追加、関数 `reviewed_renderer_installation()` 新設（`normalize()` の直後）、`preflight()` 全体置換。
- `phase172_r3r1r1_committed_renderer_guard_fix/install.py`：新規の監査パッケージ適用 Runner。
- `phase172_r3r1r1_committed_renderer_guard_fix/run.ps1`：新規。
- `phase172_r3r1r1_committed_renderer_guard_fix/tests/test_guard_fix.py`：6件の新規テスト。
- 既存の import 変更：なし。既存の本番コード・Renderer 変更：なし。

## 変更後の監査ファイル全文

監査ファイルは `corrected_audit_FULL.py` として全文を ZIP に同梱する。以下に変更した関数全体を示す。

```python
EXPECTED_HEAD_RENDERER_BLOB = '94996b403f1c01f81319824565db422463714f02'
EXPECTED_COMMITTED_R2_RENDERER_BLOB = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'

def reviewed_renderer_installation(committed_blob: str, committed: bytes, worktree: bytes) -> str:
    """Verify precisely the reviewed R2 patch, committed or not.

    The original committed baseline requires the known R2 transformation in the
    worktree. The already-committed R2 baseline requires the complete worktree
    to match that reviewed commit. No unrelated renderer variant is accepted.
    """
    from phase172_r2_suspension_relation_display.install import UPDATED_ANCHOR, transformed

    if committed_blob == EXPECTED_HEAD_RENDERER_BLOB:
        expected_worktree = transformed(committed)
        state = 'UNCOMMITTED_R2_PATCH'
    elif committed_blob == EXPECTED_COMMITTED_R2_RENDERER_BLOB:
        if normalize(committed).decode('utf-8').count(UPDATED_ANCHOR) != 1:
            raise RuntimeError('committed R2 Renderer is missing the reviewed display hook')
        expected_worktree = committed
        state = 'COMMITTED_R2_PATCH'
    else:
        raise RuntimeError('committed Renderer is neither reviewed baseline nor reviewed R2 patch')
    if normalize(worktree) != normalize(expected_worktree):
        raise RuntimeError('R2 Renderer worktree differs from its reviewed expected content')
    return state

def preflight() -> dict[str, Any]:
    branch = git('branch', '--show-current')
    head = git('rev-parse', 'HEAD')
    if branch != 'develop':
        raise RuntimeError('Phase 172 R3R1 requires develop; nothing changed')
    blob = git('rev-parse', 'HEAD:' + RENDERER.as_posix())
    committed = subprocess.run(
        ['git', 'show', 'HEAD:' + RENDERER.as_posix()],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    actual = (ROOT / RENDERER).read_bytes()
    renderer_state = reviewed_renderer_installation(blob, committed, actual)
    for path, expected_sha in (
        (R2_PROJECTION, EXPECTED_R2_PROJECTION_SHA256),
        (R2_TEST, EXPECTED_R2_TEST_SHA256),
    ):
        if not (ROOT / path).is_file() or sha256((ROOT / path).read_bytes()) != expected_sha:
            raise RuntimeError('R2R1 corrected source/test mismatch: ' + str(path))
    before = git('status', '--porcelain=v1', '--untracked-files=no')
    # Never fetch or pull automatically. Record whether the remote can be seen.
    remote = command(['git', 'ls-remote', 'origin', 'refs/heads/develop'], timeout=25)
    remote_head = (remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip()
                   else None)
    if remote_head is not None and remote_head != head:
        raise RuntimeError('origin/develop advanced; inspect current code before R3')
    return {
        'branch': branch, 'local_head': head, 'remote_develop_head': remote_head,
        'remote_reachable': remote_head is not None,
        'head_renderer_blob': blob, 'renderer_state': renderer_state,
        'r2_renderer_installed': True,
        'r2_projection_sha256': EXPECTED_R2_PROJECTION_SHA256,
        'r2_test_sha256': EXPECTED_R2_TEST_SHA256,
        'tracked_status_before': before,
    }

```

## 新規テストファイル全文

```python
"""Independent focused checks of the reviewed R3R1 renderer-state guard."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase172_r2_suspension_relation_display.install import transformed

ROOT = Path(__file__).resolve().parents[2]
REVIEWED_ORIGINAL = '94996b403f1c01f81319824565db422463714f02'
REVIEWED_COMMITTED = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'


def guard():
    path = ROOT / 'phase172_r3r1r1_committed_renderer_guard_fix/corrected_audit_FULL.py'
    tree = ast.parse(path.read_text(encoding='utf-8'))
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in ('normalize', 'reviewed_renderer_installation')]
    assert len(nodes) == 2
    space = {
        'EXPECTED_HEAD_RENDERER_BLOB': REVIEWED_ORIGINAL,
        'EXPECTED_COMMITTED_R2_RENDERER_BLOB': REVIEWED_COMMITTED,
    }
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), space)
    return space['reviewed_renderer_installation']


def original():
    return (
        'def render_model_backed_narrative_markdown():\n'
        '    if direct_sum_display is not None:\n'
        '        suppressed_body_indices.update(direct_sum_display.hidden_indices)\n'
        '    for index in order:\n'
        '        pass\n'
    ).encode('utf-8')


def test_committed_r2_content_is_accepted_only_as_exact_match():
    before = original()
    after = transformed(before)
    assert guard()(REVIEWED_COMMITTED, after, after) == 'COMMITTED_R2_PATCH'


def test_uncommitted_r2_content_is_accepted_when_patched():
    before = original()
    after = transformed(before)
    assert guard()(REVIEWED_ORIGINAL, before, after) == 'UNCOMMITTED_R2_PATCH'


def test_worktree_change_is_rejected_even_if_r2_committed():
    after = transformed(original())
    with pytest.raises(RuntimeError, match='worktree differs'):
        guard()(REVIEWED_COMMITTED, after, after + b'# unrelated\n')


def test_missing_r2_hook_is_rejected_for_committed_case():
    before = original()
    with pytest.raises(RuntimeError, match='missing the reviewed display hook'):
        guard()(REVIEWED_COMMITTED, before, before)


def test_unknown_committed_blob_is_rejected():
    after = transformed(original())
    with pytest.raises(RuntimeError, match='neither reviewed baseline'):
        guard()('0000000000000000000000000000000000000000', after, after)


def test_windows_crlf_worktree_is_accepted_for_committed_case():
    after = transformed(original())
    assert guard()(REVIEWED_COMMITTED, after, after.replace(b'\n', b'\r\n')) == 'COMMITTED_R2_PATCH'

```

## 新規 installer 全文

```python
"""Phase 172 R3R1R1: guarded correction to read-only audit preflight only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / 'phase172_r3r1_hopf_chain_audit/audit.py'
CORRECTED = PACKAGE / 'corrected_audit_FULL.py'
ORIGINAL_SHA256 = 'dd7ce74dd6a367209a49349f2b6a95ff73496a6f1febcc51059abb4bc7555907'
CORRECTED_SHA256 = 'a5110955a0d98b9ec46663ce64bdedfba92938f254490a2c67d34baa67dbfad5'


def normalized(raw: bytes) -> bytes:
    source = raw.decode('utf-8-sig')
    if '\r' in source.replace('\r\n', ''):
        raise RuntimeError('mixed source newlines are unsupported')
    return source.replace('\r\n', '\n').encode('utf-8')


def sha256(raw: bytes) -> str:
    return hashlib.sha256(normalized(raw)).hexdigest()


def preflight() -> tuple[str, str, bytes, bytes]:
    result = subprocess.run(['git', 'branch', '--show-current'], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    if result.stdout.strip() != 'develop':
        raise RuntimeError('correction requires develop; no files changed')
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    if not TARGET.is_file() or not CORRECTED.is_file():
        raise RuntimeError('R3R1 source or correction payload is missing')
    current = TARGET.read_bytes()
    replacement = CORRECTED.read_bytes()
    if sha256(replacement) != CORRECTED_SHA256:
        raise RuntimeError('bundled reviewed corrected source mismatch')
    current_sha = sha256(current)
    if current_sha not in (ORIGINAL_SHA256, CORRECTED_SHA256):
        raise RuntimeError('unreviewed R3R1 audit content; refusing replacement')
    return head, ('ALREADY_CORRECTED' if current_sha == CORRECTED_SHA256 else 'NEEDS_CORRECTION'), current, replacement


def command(args: list[str], report: Path, filename: str) -> None:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    run = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                         encoding='utf-8', errors='replace', env=env, check=False)
    log = run.stdout + '\n' + run.stderr
    (report / filename).write_text(log, encoding='utf-8')
    print(log[-3000:], flush=True)
    if run.returncode:
        raise RuntimeError(f'command failed (exit {run.returncode}): {filename}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    args = parser.parse_args()
    head, state, original, replacement = preflight()
    print('PHASE172_R3R1R1_BRANCH=develop', flush=True)
    print('PHASE172_R3R1R1_HEAD=' + head, flush=True)
    print('PHASE172_R3R1R1_PAYLOAD_GUARD=PASS', flush=True)
    print('PHASE172_R3R1R1_AUDIT_SOURCE_STATE=' + state, flush=True)
    if args.dry_run:
        print('PHASE172_R3R1R1_SOURCE_CHANGES=0', flush=True)
        print('PHASE172_R3R1R1_DRY_RUN=PASS', flush=True)
        return 0
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    report = base / ('phase172_r3r1r1_' + stamp)
    report.mkdir(parents=True, exist_ok=False)
    (report / 'audit.py.before').write_bytes(original)
    modified = state != 'ALREADY_CORRECTED'
    try:
        if modified:
            ending = b'\r\n' if b'\r\n' in original else b'\n'
            TARGET.write_bytes(normalized(replacement).replace(b'\n', ending))
        if sha256(TARGET.read_bytes()) != CORRECTED_SHA256:
            raise RuntimeError('post-write content mismatch')
        print('PHASE172_R3R1R1_AUDIT_GUARD_CORRECTED=PASS', flush=True)
        if args.run_focused_tests:
            command([sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                     'phase172_r3r1r1_committed_renderer_guard_fix/tests/test_guard_fix.py'],
                    report, 'focused_guard.log')
            print('PHASE172_R3R1R1_GUARD_TESTS=PASS', flush=True)
        audit_args = [sys.executable, '-B', '-m', 'phase172_r3r1_hopf_chain_audit.audit']
        if args.run_focused_tests:
            audit_args.append('--run-focused-tests')
        command(audit_args, report, 'hopf_audit.log')
        print('PHASE172_R3R1R1_RESULT=PASS_CORRECTED_R3R1_AUDIT', flush=True)
        print('PHASE172_R3R1R1_REPORT=' + str(report), flush=True)
        return 0
    except Exception as error:
        if modified:
            TARGET.write_bytes(original)
            print('PHASE172_R3R1R1_RESTORED=PASS', flush=True)
        print('PHASE172_R3R1R1_RESULT=FAIL', flush=True)
        print('PHASE172_R3R1R1_REPORT=' + str(report), flush=True)
        print('PHASE172_R3R1R1_DIAGNOSTIC=' + repr(error), flush=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())

```

## 新規 PowerShell Runner 全文

```powershell
param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPythonPath = $env:PYTHONPATH
$OldUTF8 = $env:PYTHONUTF8
$OldIOEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r3r1r1_committed_renderer_guard_fix.install')
    if ($DryRun) { $Arguments += '--dry-run' }
    if ($RunFocusedTests) { $Arguments += '--run-focused-tests' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R3R1R1 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONUTF8 = $OldUTF8
    $env:PYTHONIOENCODING = $OldIOEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}

```
