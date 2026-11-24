# R3R39R2 追加コード全文

既存コード変更なし。新規ディレクトリ直下に追加。

## guard.py

```python
"""Verify the exact R3R39 change independently of Git staging state."""
from __future__ import annotations

import argparse
import subprocess

from phase176_r3r39_public_equality_transport.apply import (
    ROOT, TARGET, normalized_source, patched_bytes,
)

BASE = "8033d70c5ee67626b278918be15484c688ed146e"


def classify(baseline: bytes, head: bytes, index: bytes, current: bytes) -> str:
    expected = patched_bytes(baseline, current)
    if expected == baseline or normalized_source(expected) == normalized_source(baseline):
        raise ValueError("BASELINE_ALREADY_PATCHED")
    if current != expected:
        raise ValueError("WORKTREE_BYTES_NOT_REPAIRED")
    if head == baseline and index == baseline:
        return "UNSTAGED"
    if head == baseline and index == expected:
        return "STAGED"
    if head == expected and index == expected:
        return "COMMITTED"
    raise ValueError("UNEXPECTED_HEAD_OR_INDEX_BYTES")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    relative = TARGET.relative_to(ROOT).as_posix()
    def read_git(spec: str) -> bytes:
        return subprocess.check_output(["git", "show", spec], cwd=ROOT)
    baseline = read_git(BASE + ":" + relative)
    head = read_git("HEAD:" + relative)
    index = read_git(":" + relative)
    current = TARGET.read_bytes()
    state = classify(baseline, head, index, current)
    # Check actual Git reporting as well; fail rather than hide index flags or filters.
    def stat(*options: str) -> str:
        return subprocess.check_output(["git", "diff", *options, "--numstat", "--", relative], cwd=ROOT).decode("utf-8").strip()
    expected_stat = "9\t0\t" + relative
    expected = {"UNSTAGED": (expected_stat, ""), "STAGED": ("", expected_stat), "COMMITTED": ("", "")}[state]
    actual = (stat(), stat("--cached"))
    if actual != expected:
        raise ValueError(f"GIT_DIFF_STATE_MISMATCH: state={state}, actual={actual!r}, expected={expected!r}")
    if stat(BASE) != expected_stat:
        raise ValueError("BASELINE_DIFF_NOT_NINE_INSERTIONS")
    print("PHASE176_R3R39R2_GIT_STATE=" + state)
    print("PHASE176_R3R39R2_BASELINE_DIFF=" + expected_stat)
    print("PHASE176_R3R39R2_GATE=" + ("PASS_R3R39R2_DRYRUN" if args.dry_run else "PASS_R3R39R2_EXACT_PATCH_VERIFIED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $guardArgs = @()
    if ($DryRun) { $guardArgs += '--dry-run' }
    & python -B -m phase176_r3r39r2_git_state_guard.guard @guardArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R2 git state guard failed' }
    if ($DryRun) { return }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'worktree diff check failed' }
    & git diff --cached --check
    if ($LASTEXITCODE -ne 0) { throw 'index diff check failed' }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib .\phase176_r3r39r2_git_state_guard\test_guard.py .\phase176_r3r39r1_eol_repair\test_eol.py
    if ($LASTEXITCODE -ne 0) { throw 'Git state and EOL tests failed' }
    & python -B -m phase176_r3r39_public_equality_transport.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 DFS audit failed' }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        .\phase176_r3r39_public_equality_transport\tests\test_source.py `
        .\phase176_r3r38_equality_transport_isolated\tests\test_source.py `
        .\phase176_r3r34_composite_suspension_isolated\tests\test_source.py `
        .\phase176_r3r36_composite_right_hopf_isolated\tests\test_source.py `
        .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 focused tests failed' }
    Write-Host 'PHASE176_R3R39R2_GATE=PASS_R3R39R2_EXACT_PATCH_FOCUSED_TESTS'
    Write-Host 'PHASE176_R3R39R2_FULL_PYTEST=NOT_RUN'
    Write-Host '(END)'
} finally {
    Pop-Location
}

```

## test_guard.py

```python
import pytest

from phase176_r3r39_public_equality_transport.apply import (
    INSERT_AFTER_AVAILABLE, INSERT_AFTER_HOPF, updated_source,
)
from phase176_r3r39r2_git_state_guard.guard import classify


def inputs():
    original = (
        "def f(prior_conclusions, goal, available):\n"
        + INSERT_AFTER_AVAILABLE + "        pass\n"
        + "    if True:\n"
        + "        options.extend(expand_composite_suspension_equality(goal))\n"
        + INSERT_AFTER_HOPF
    )
    return original.encode(), updated_source(original).encode()


@pytest.mark.parametrize("state", ["UNSTAGED", "STAGED", "COMMITTED"])
def test_exact_change_in_each_git_state(state):
    original, expected = inputs()
    head = expected if state == "COMMITTED" else original
    index = original if state == "UNSTAGED" else expected
    assert classify(original, head, index, expected) == state


def test_missing_patch_rejected():
    original, _ = inputs()
    with pytest.raises(ValueError, match="WORKTREE_BYTES_NOT_REPAIRED"):
        classify(original, original, original, original)


def test_unrelated_index_rejected():
    original, expected = inputs()
    with pytest.raises(ValueError, match="UNEXPECTED_HEAD_OR_INDEX_BYTES"):
        classify(original, original, expected + b"# unrelated\n", expected)


def test_wrong_eol_rejected():
    original, expected = inputs()
    with pytest.raises(ValueError, match="WORKTREE_BYTES_NOT_REPAIRED"):
        classify(original, original, original, expected.replace(b"\n", b"\r\n"))

```

## README.md

```markdown
# Phase 176 R3R39R2

Read-only Git state guard for the exact nine-line R3R39 patch. Accepts unstaged, staged, or committed changes only when the worktree, HEAD, index and baseline diff agree. The baseline is the previously verified develop commit 8033d70c5ee67626b278918be15484c688ed146e. No production code is written and no Git staging or commit is performed. Requires the R3R39 and R3R39R1 packages already extracted. Run `run.ps1 -DryRun`, then `run.ps1`. Full pytest is not run.

```
