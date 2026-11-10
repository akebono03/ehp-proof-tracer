# Phase 174 R55R1 変更コード全文

## 変更対象

- 既存 `phase174_r3_r7_r55_common_exactness_intro/source_guard.py`: `verify_checkout()` の比較式1箇所を修正（関数全文は以下）。`import` 変更なし。
- 新規 `phase174_r3_r7_r55r1_source_guard_type_fix/patch.py`: `normalized_bytes()`、`digest()`、`safe_git()`、`validate_repository()`、`corrected_source()`、`apply_fix()`、`main()`（各関数全文、追加位置は新規ファイル）。
- 新規 `phase174_r3_r7_r55r1_source_guard_type_fix/tests/test_fix.py`: `test_exactly_one_comparison_changed_without_restructuring()`、`test_windows_crlf_is_preserved_and_replay_is_idempotent()`、`test_unreviewed_partial_or_unrelated_changes_are_rejected()`、`test_complete_guard_accepts_uninstalled_baseline()`、`test_complete_guard_accepts_installed_patch()`（新規テストファイル内）。
- 新規 `phase174_r3_r7_r55r1_source_guard_type_fix/run.ps1`: 実行用スクリプト。

## `source_guard.py` 修正後全文

```python
"""R55: pin the GitHub-reviewed mathematical and common-Renderer sources."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'phase168_r3_5_model_renderer.py'
REVIEWED_HEAD = '40db3a00ca8be58e589e0949e6a70dcedd3b9cf5'
BLOBS = {
    TARGET: '64e0570e8462ee0361ed07afab836c66ce8e7895',
    'phase168_r3_26_exactness_projection.py': 'a62fef3bce2150510e1c487ac6c381227b9a0860',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'web_app.py': '6f95663df5cbf028bb16d1f05dca62db2e3fc00e',
    'templates/index.html': '7af2afa40b92b8c1ec3916cf9759516c158b989f',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_r3_web_adapter.py': 'dda215780c0468cf421592aff86c79b1f5482eed',
    'phase174_r3_r7_r54_public_http_narrative_audit/audit.py': '505192a0e166672908322a8e6a2de4f59f23a6ab',
    'phase174_r3_r7_r54_public_http_narrative_audit/tests/test_http.py': 'f7c72f95d055a9d9fd7f7f13529b740a6c431334',
}


def git(*args: str) -> bytes:
    proc = subprocess.run(('git',) + args,cwd=ROOT,capture_output=True,check=True)
    return proc.stdout


def sha_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Verify HEAD, index, all reviewed blobs, and the exact renderer patch."""
    from phase174_r3_r7_r55_common_exactness_intro.patch import replace_lines_preserving_eol
    if Path(git('rev-parse','--show-toplevel').decode().strip()).resolve()!=ROOT.resolve():
        raise RuntimeError('R55 directory must be unpacked under repo root')
    if git('branch','--show-current').decode().strip()!='develop':
        raise RuntimeError('R55 expects develop')
    head=git('rev-parse','HEAD').decode().strip()
    remote=git('ls-remote','origin','refs/heads/develop').decode().strip().split()
    if head!=REVIEWED_HEAD or not remote or remote[0]!=REVIEWED_HEAD:
        raise RuntimeError('R55 requires the reviewed live GitHub develop HEAD')
    if git('diff','--cached','--name-only').strip():
        raise RuntimeError('Staged files require separate review')
    changed=tuple(git('diff','--name-only').decode().splitlines())
    if changed not in ((),(TARGET,)):
        raise RuntimeError('R55 found unrelated tracked edits: '+repr(changed))
    for file,blob in BLOBS.items():
        baseline=git('show','HEAD:'+file)
        if sha_blob(baseline)!=blob:
            raise RuntimeError('Reviewed GitHub mathematical or renderer source changed: '+file)
        actual=(ROOT/file).read_bytes()
        if file != TARGET and actual.replace(b'\r\n',b'\n')!=baseline.replace(b'\r\n',b'\n'):
            raise RuntimeError('Tracked source differs from GitHub HEAD: '+file)
    previous=git('show','HEAD:'+TARGET)
    actual=(ROOT/TARGET).read_bytes()
    def norm(blob:bytes)->str:
        return blob.decode('utf-8-sig').replace('\r\n','\n')
    desired=replace_lines_preserving_eol(norm(previous))
    installed=(norm(actual)==desired)
    if changed==() and norm(actual)!=norm(previous):
        raise RuntimeError('Renderer changed without Git status evidence')
    if changed==(TARGET,) and not installed:
        raise RuntimeError('Unreviewed renderer edit or mixed patch')
    return {
        'source_guard':'PASS', 'local_head':head,'remote_head':remote[0],
        'reviewed_blobs':len(BLOBS),'tracked_changes':changed,
        'r55_renderer_installed':installed,
        'new_given':0,'new_mathematical_rules':0,'full_pytest':False,
    }
```

## `patch.py` 新規全文

```python
"""R55R1: fix only str-vs-bytes comparison inside R55 Source Guard.

The original R55 renderer patch and inference pipeline remain unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / 'phase174_r3_r7_r55_common_exactness_intro' / 'source_guard.py'
R55_PATCH = ROOT / 'phase174_r3_r7_r55_common_exactness_intro' / 'patch.py'
REVIEWED_HEAD = '40db3a00ca8be58e589e0949e6a70dcedd3b9cf5'
BEFORE_SHA256 = '6b5edb3268c05d98fffdb2c8fcd067711d71aeaca53d67ab4b260a8ea16a02ac'
AFTER_SHA256 = 'f3f2734a99eeb2b151ada8924a461d3666dc2bc914526564498fa2dc37a562fa'
R55_PATCH_SHA256 = '2fb88d528e4f884780cf8428ae0e49754318032d029843aed91a67f6008b2c80'
BEFORE_EXPRESSION = 'installed=(norm(actual)==norm(desired))'
AFTER_EXPRESSION = 'installed=(norm(actual)==desired)'


def normalized_bytes(blob: bytes) -> bytes:
    """Treat Windows and Unix end-of-line conventions alike."""
    return blob.replace(b'\r\n', b'\n')


def digest(blob: bytes) -> str:
    """Hash exactly the normalized UTF-8 bytes of a reviewed file."""
    return hashlib.sha256(normalized_bytes(blob)).hexdigest()


def safe_git(*args: str) -> str:
    """Return a Git observation; never stage, reset, clean or commit."""
    process = subprocess.run(
        ('git',) + args, cwd=ROOT, capture_output=True,
        check=True, encoding='utf-8', errors='replace',
    )
    return process.stdout.strip()


def validate_repository() -> dict[str, object]:
    """Require the R54 merged HEAD and only R55's reviewed renderer edit."""
    if Path(safe_git('rev-parse', '--show-toplevel')).resolve() != ROOT.resolve():
        raise RuntimeError('R55R1 must be extracted immediately inside repository root')
    if safe_git('branch', '--show-current') != 'develop':
        raise RuntimeError('R55R1 requires develop')
    local_head = safe_git('rev-parse', 'HEAD')
    remote_line = safe_git('ls-remote', 'origin', 'refs/heads/develop').splitlines()
    remote_head = remote_line[0].split()[0] if remote_line else ''
    if local_head != REVIEWED_HEAD or remote_head != REVIEWED_HEAD:
        raise RuntimeError('R55R1 requires reviewed local/remote develop HEAD')
    if safe_git('diff', '--cached', '--name-only'):
        raise RuntimeError('R55R1 forbids staged file changes')
    modified = tuple(safe_git('diff', '--name-only').splitlines())
    if modified not in ((), ('phase168_r3_5_model_renderer.py',)):
        raise RuntimeError('Unreviewed tracked changes: ' + repr(modified))
    if not R55_PATCH.is_file() or digest(R55_PATCH.read_bytes()) != R55_PATCH_SHA256:
        raise RuntimeError('R55 original patch.py source differs from reviewed ZIP')
    if not TARGET.is_file():
        raise RuntimeError('R55 source_guard.py must already be extracted')
    source = TARGET.read_bytes()
    current = digest(source)
    if current not in (BEFORE_SHA256, AFTER_SHA256):
        raise RuntimeError('R55 source guard is neither reviewed before nor after source')
    return {
        'local_head': local_head,
        'remote_head': remote_head,
        'tracked_changes': modified,
        'source_guard_state': 'FIXED' if current == AFTER_SHA256 else 'ORIGINAL',
        'new_givens': 0,
        'new_mathematical_rules': 0,
        'production_files_changed': 0,
        'full_pytest': False,
    }


def corrected_source(source: bytes) -> bytes:
    """Apply the reviewed one-expression change, preserving line endings."""
    decoded = normalized_bytes(source).decode('utf-8-sig')
    if decoded.count(AFTER_EXPRESSION) == 1 and decoded.count(BEFORE_EXPRESSION) == 0:
        return source
    if decoded.count(BEFORE_EXPRESSION) != 1 or decoded.count(AFTER_EXPRESSION) != 0:
        raise RuntimeError('R55R1 reviewed expression occurs an unexpected number of times')
    result = source.replace(BEFORE_EXPRESSION.encode('utf-8'), AFTER_EXPRESSION.encode('utf-8'), 1)
    if digest(result) != AFTER_SHA256:
        raise RuntimeError('R55R1 result differs from reviewed complete source')
    return result


def apply_fix(*, dry_run: bool = False) -> dict[str, object]:
    """Apply only the R55 guard fix; support repeated dry/run invocations."""
    state = validate_repository()
    before = TARGET.read_bytes()
    after = corrected_source(before)
    if not dry_run and before != after:
        TARGET.write_bytes(after)
    if not dry_run:
        final = validate_repository()
        if final['source_guard_state'] != 'FIXED':
            raise RuntimeError('R55R1 fix failed postcondition')
    return {
        **state,
        'dry_run': dry_run,
        'source_guard_fixed': (not dry_run),
        'source_guard_already_fixed': before == after,
        'modified_files': 0 if dry_run or before == after else 1,
        'target': 'phase174_r3_r7_r55_common_exactness_intro/source_guard.py',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    state = apply_fix(dry_run=args.dry_run)
    prefix = 'PHASE174_R3R7R55R1_'
    for key, value in state.items():
        print(prefix + key.upper() + '=' + str(value))
    print(prefix + 'GATE=' + (
        'PASS_R55R1_SOURCE_GUARD_DRYRUN' if args.dry_run else
        'PASS_R55R1_SOURCE_GUARD_FIXED'
    ))
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## `tests/test_fix.py` 新規全文

```python
"""R55R1 checks exact source replacement and the real guard's two states."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r55r1_source_guard_type_fix import patch

PACKAGE = Path(__file__).resolve().parents[1]


def _source_bytes(name: str) -> bytes:
    return (PACKAGE / name / 'source_guard.py').read_bytes()


def test_exactly_one_comparison_changed_without_restructuring() -> None:
    before = _source_bytes('baseline')
    after = _source_bytes('replacement')
    assert patch.digest(before) == patch.BEFORE_SHA256
    assert patch.digest(after) == patch.AFTER_SHA256
    assert patch.corrected_source(before) == after
    assert patch.corrected_source(after) == after
    assert patch.BEFORE_EXPRESSION.encode('utf-8') in before
    assert patch.AFTER_EXPRESSION.encode('utf-8') in after
    assert before.replace(
        patch.BEFORE_EXPRESSION.encode('utf-8'),
        patch.AFTER_EXPRESSION.encode('utf-8'), 1,
    ) == after
    ast.parse(after.decode('utf-8'))


def test_windows_crlf_is_preserved_and_replay_is_idempotent() -> None:
    before = _source_bytes('baseline').replace(b'\n', b'\r\n')
    after = patch.corrected_source(before)
    assert patch.digest(after) == patch.AFTER_SHA256
    assert after == _source_bytes('replacement').replace(b'\n', b'\r\n')
    assert patch.corrected_source(after) == after


def test_unreviewed_partial_or_unrelated_changes_are_rejected() -> None:
    with pytest.raises(RuntimeError):
        patch.corrected_source(_source_bytes('baseline').replace(
            patch.BEFORE_EXPRESSION.encode('utf-8'), b'installed=True', 1,
        ))
    with pytest.raises(RuntimeError):
        patch.corrected_source(_source_bytes('baseline').replace(
            b"return {", b"return {'unexpected': 1,", 1,
        ))


def _mock_checkout(monkeypatch, tmp_path: Path, *, installed: bool) -> dict[str, object]:
    """Execute the complete revised guard with a realistic fake Git checkout."""
    import runpy
    guard_globals = runpy.run_path(str(PACKAGE / 'replacement' / 'source_guard.py'))
    original = b'\n'.join((
        b'def render_model_backed_narrative_markdown(result, model):',
        b'    for chain in chains:',
        b'        exactness_numbers = (3,)',
        b'        if exactness_numbers:',
        b'            tags = ", ".join(f"[R{number}]" for number in exactness_numbers)',
        '            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, {tags}を用いて次の完全列を考える.")'.encode('utf-8'),
        b'        else:',
        '            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, 次の完全列を考える.")'.encode('utf-8'),
        b'    return lines', b'',
    ))
    from phase174_r3_r7_r55_common_exactness_intro.patch import replace_lines_preserving_eol
    desired = replace_lines_preserving_eol(original.decode('utf-8')).encode('utf-8')
    target = guard_globals['TARGET']
    extra_name = 'extra.txt'
    tree = tmp_path / 'repo'
    tree.mkdir()
    (tree / target).write_bytes(desired if installed else original)
    (tree / extra_name).write_bytes(b'unchanged\n')
    baseline_blobs = {target: original, extra_name: b'unchanged\n'}
    dummy_sha = {name: guard_globals['sha_blob'](contents)
                 for name, contents in baseline_blobs.items()}
    head = guard_globals['REVIEWED_HEAD']
    changed = (target,) if installed else ()

    def fake_git(*args: str) -> bytes:
        if args == ('rev-parse', '--show-toplevel'):
            return str(tree).encode('utf-8') + b'\n'
        if args == ('branch', '--show-current'):
            return b'develop\n'
        if args == ('rev-parse', 'HEAD'):
            return head.encode('ascii') + b'\n'
        if args == ('ls-remote', 'origin', 'refs/heads/develop'):
            return head.encode('ascii') + b'\trefs/heads/develop\n'
        if args == ('diff', '--cached', '--name-only'):
            return b''
        if args == ('diff', '--name-only'):
            return b''.join(item.encode('utf-8') + b'\n' for item in changed)
        if len(args) == 2 and args[0] == 'show' and args[1].startswith('HEAD:'):
            return baseline_blobs[args[1][5:]]
        raise AssertionError(args)

    # The function keeps its original module globals, which runpy returns as a
    # dictionary only after running the module; override them in place via
    # the underlying function globals (no project production imports patched).
    guard = guard_globals['verify_checkout']
    guard.__globals__['ROOT'] = tree
    guard.__globals__['BLOBS'] = dummy_sha
    guard.__globals__['git'] = fake_git
    return guard()


def test_complete_guard_accepts_uninstalled_baseline(monkeypatch, tmp_path: Path) -> None:
    observed = _mock_checkout(monkeypatch, tmp_path, installed=False)
    assert observed['source_guard'] == 'PASS'
    assert observed['r55_renderer_installed'] is False
    assert observed['tracked_changes'] == ()


def test_complete_guard_accepts_installed_patch(monkeypatch, tmp_path: Path) -> None:
    observed = _mock_checkout(monkeypatch, tmp_path, installed=True)
    assert observed['source_guard'] == 'PASS'
    assert observed['r55_renderer_installed'] is True
    assert observed['tracked_changes'] == ('phase168_r3_5_model_renderer.py',)
```

## `run.ps1` 新規全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r55r1_source_guard_type_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55R1 Source Guard preflight failed' }

    Write-Output 'PHASE174_R3R7R55R1_TEST_GROUP=R55R1_TYPE_FIX'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r55r1_source_guard_type_fix/tests/test_fix.py
    if ($LASTEXITCODE -ne 0) { throw 'R55R1 focused test contract failed' }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R55R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }

    python -B -m phase174_r3_r7_r55r1_source_guard_type_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R55R1 Source Guard repair failed' }

    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r55_common_exactness_intro\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R55 repaired DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r55_common_exactness_intro\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R55 repaired full audit or focused pytest failed' }

    Write-Output 'PHASE174_R3R7R55R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R55R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
