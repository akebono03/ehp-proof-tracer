# R3R39R3 — 追加コード全文

新規ディレクトリ内に以下のファイルを配置する。既存の数学規則と共有探索関数は変更しない。

## repair.py

```python
"""Repair only R3R39 line endings against its immutable pre-change Git blob."""
from __future__ import annotations

import argparse
import difflib
import subprocess
from pathlib import Path

from phase176_r3r39_public_equality_transport.apply import updated_source

ROOT = Path(__file__).resolve().parent.parent
TARGET = 'phase165_r52_r9_shared_math.py'
BASE = '8033d70c5ee67626b278918be15484c688ed146e'
BASE_BLOB = '359fc9e6be767d4b8b48549213a69244c4dbf7ce'


def expected_bytes(baseline: bytes) -> bytes:
    if b'\r' in baseline or baseline.startswith(b'\xef\xbb\xbf'):
        raise ValueError('UNEXPECTED_BASELINE_ENCODING')
    text = baseline.decode('utf-8')
    patched = updated_source(text)
    changes = list(difflib.ndiff(text.splitlines(keepends=True),
                                patched.splitlines(keepends=True)))
    if sum(s.startswith('+ ') for s in changes) != 9 or any(
            s.startswith('- ') for s in changes):
        raise ValueError('EXPECTED_EXACT_NINE_INSERTIONS')
    return patched.encode('utf-8')


def representation(raw: bytes, expected: bytes) -> str:
    if raw == expected:
        return 'LF'
    if raw == expected.replace(b'\n', b'\r\n'):
        return 'CRLF'
    raise ValueError('UNRELATED_OR_INCOMPLETE_SOURCE_REFUSED')


def git(root: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.check_output(['git', *args], cwd=root, input=data)


def inspect(root: Path, baseline: bytes, *, dry_run: bool) -> dict[str, str]:
    expected = expected_bytes(baseline)
    path = root / TARGET
    head = git(root, 'show', 'HEAD:' + TARGET)
    index = git(root, 'show', ':' + TARGET)
    current = path.read_bytes()
    states = {name: representation(raw, expected) for name, raw in (
        ('HEAD', head), ('INDEX', index), ('WORKTREE', current))}
    if head != index and index != expected:
        raise ValueError('UNEXPECTED_STAGED_REPRESENTATION')
    # Verify Git's actual clean conversion before any write. No object is stored.
    desired_hash = git(root, 'hash-object', '--stdin', '--no-filters', data=expected)
    filtered_hash = git(root, 'hash-object', '--stdin', '--path=' + TARGET, data=expected)
    if filtered_hash != desired_hash:
        raise ValueError('GIT_FILTER_WOULD_CHANGE_EXPECTED_LF_BLOB')
    if not dry_run and current != expected:
        path.write_bytes(expected)
    if not dry_run and path.read_bytes() != expected:
        raise ValueError('WORKTREE_WRITE_VERIFICATION_FAILED')
    states['WORKTREE_AFTER'] = representation(path.read_bytes(), expected)
    states['EXPECTED_BLOB'] = desired_hash.decode('ascii').strip()
    states['COMMIT_REQUIRED'] = str(head != expected)
    return states


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if git(ROOT, 'rev-parse', BASE + ':' + TARGET).decode('ascii').strip() != BASE_BLOB:
        raise ValueError('BASELINE_BLOB_MISMATCH')
    baseline = git(ROOT, 'show', BASE + ':' + TARGET)
    states = inspect(ROOT, baseline, dry_run=args.dry_run)
    for key, value in states.items():
        print('PHASE176_R3R39R3_' + key + '=' + value)
    print('PHASE176_R3R39R3_GATE=' + ('PASS_R3R39R3_DRYRUN' if args.dry_run else 'PASS_R3R39R3_FIXED_BASELINE_WORKTREE'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## test_repair.py

```python
from pathlib import Path

import pytest

from phase176_r3r39_public_equality_transport.apply import (
    INSERT_AFTER_AVAILABLE, INSERT_AFTER_HOPF,
)
from phase176_r3r39r3_fixed_baseline_repair.repair import (
    TARGET, expected_bytes, git, inspect, representation,
)


def baseline() -> bytes:
    return ('def f(prior_conclusions, goal, available):\n'
            + INSERT_AFTER_AVAILABLE + '        pass\n'
            + '    if True:\n'
            + '        options.extend(expand_composite_suspension_equality(goal))\n'
            + INSERT_AFTER_HOPF).encode()


def repo(path: Path, autocrlf: str) -> bytes:
    expected = expected_bytes(baseline())
    git(path, 'init', '-q')
    git(path, 'config', 'user.name', 'Test')
    git(path, 'config', 'user.email', 'test@example.invalid')
    git(path, 'config', 'core.autocrlf', 'false')
    (path / TARGET).write_bytes(expected.replace(b'\n', b'\r\n'))
    git(path, 'add', '--', TARGET)
    git(path, 'commit', '-qm', 'CRLF commit')
    git(path, 'config', 'core.autocrlf', autocrlf)
    return expected


@pytest.mark.parametrize('autocrlf', ['false', 'true', 'input'])
def test_committed_crlf_repair(tmp_path, autocrlf):
    expected = repo(tmp_path, autocrlf)
    before = git(tmp_path, 'rev-parse', 'HEAD')
    dry = inspect(tmp_path, baseline(), dry_run=True)
    assert dry['WORKTREE_AFTER'] == 'CRLF'
    result = inspect(tmp_path, baseline(), dry_run=False)
    assert result['HEAD'] == 'CRLF'
    assert result['WORKTREE_AFTER'] == 'LF'
    assert (tmp_path / TARGET).read_bytes() == expected
    assert git(tmp_path, 'rev-parse', 'HEAD') == before
    assert git(tmp_path, 'show', ':' + TARGET) != expected
    git(tmp_path, 'add', '--', TARGET)
    assert git(tmp_path, 'show', ':' + TARGET) == expected
    git(tmp_path, 'commit', '-qm', 'LF repair')
    assert inspect(tmp_path, baseline(), dry_run=False)['COMMIT_REQUIRED'] == 'False'


def test_unrelated_worktree_refused(tmp_path):
    expected = repo(tmp_path, 'false')
    wrong = expected + b'# unrelated\n'
    (tmp_path / TARGET).write_bytes(wrong)
    with pytest.raises(ValueError, match='UNRELATED_OR_INCOMPLETE'):
        inspect(tmp_path, baseline(), dry_run=False)
    assert (tmp_path / TARGET).read_bytes() == wrong


def test_missing_patch_refused():
    with pytest.raises(ValueError, match='UNRELATED_OR_INCOMPLETE'):
        representation(baseline(), expected_bytes(baseline()))


def test_mixed_eol_refused():
    expected = expected_bytes(baseline())
    with pytest.raises(ValueError, match='UNRELATED_OR_INCOMPLETE'):
        representation(expected.replace(b'\n', b'\r\n', 1), expected)
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $arguments = @()
    if ($DryRun) { $arguments += '--dry-run' }
    & python -B -m phase176_r3r39r3_fixed_baseline_repair.repair @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R3 fixed baseline repair failed' }
    if ($DryRun) { return }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib .\phase176_r3r39r3_fixed_baseline_repair\test_repair.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R3 focused tests failed' }
    & python -B -m phase176_r3r39_public_equality_transport.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 DFS audit failed' }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        .\phase176_r3r39_public_equality_transport\tests\test_source.py `
        .\phase176_r3r38_equality_transport_isolated\tests\test_source.py `
        .\phase176_r3r34_composite_suspension_isolated\tests\test_source.py `
        .\phase176_r3r36_composite_right_hopf_isolated\tests\test_source.py `
        .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 focused tests failed' }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'git diff check failed' }
    Write-Host 'PHASE176_R3R39R3_GATE=PASS_R3R39R3_FIXED_BASELINE_FOCUSED_TESTS'
    Write-Host 'PHASE176_R3R39R3_FULL_PYTEST=NOT_RUN'
    Write-Host '(END)'
} finally {
    Pop-Location
}
```
