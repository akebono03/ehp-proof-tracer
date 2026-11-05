# Phase 174 R3-R6-R3R2 完全コード

以下は新規ファイルの全文です。既存 import・クラス・関数の変更はありません。

## 新規 `run.ps1`

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    $reviewedHead = 'ecbb2fea225c5b88000629d9c025934fcc2d7075'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R3-R6-R3R2 requires develop.'
    }
    git fetch origin
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify origin/develop.' }
    $localHead = (git rev-parse HEAD).Trim()
    $remoteHead = (git rev-parse origin/develop).Trim()
    if ($LASTEXITCODE -ne 0 -or $localHead -ne $reviewedHead -or $remoteHead -ne $reviewedHead) {
        throw "Unreviewed HEAD: local=$localHead remote=$remoteHead reviewed=$reviewedHead"
    }
    Write-Output "PHASE174_R3R6R3R2_BRANCH=$branch"
    Write-Output "PHASE174_R3R6R3R2_LOCAL_HEAD=$localHead"
    Write-Output "PHASE174_R3R6R3R2_REMOTE_HEAD=$remoteHead"

    # This is a check, not the earlier --apply operation.  The prior apply
    # already succeeded and must not be run a second time.
    python -m phase174_r3_r6_r3r2_pytest_importmode_fix.verify
    if ($LASTEXITCODE -ne 0) {
        throw 'Previously applied common Renderer differs from reviewed implementation.'
    }

    $testFiles = @(
        'phase174_r3_r6_r3r2_pytest_importmode_fix/tests/test_r3r2_importmode.py',
        'phase174_r3_r6_r3r1_scoped_guard_fix/tests/test_patch.py',
        'phase174_r3_r6_r3_common_narrative/tests/test_projection.py',
        'phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py',
        'phase174_r3_r6_source_extension/tests/test_source.py',
        'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
        'phase172_r5_prior_reference_display/tests/test_projection.py'
    )
    foreach ($testFile in $testFiles) {
        if (-not (Test-Path $testFile -PathType Leaf)) {
            throw "Missing focused test file: $testFile"
        }
    }
    Write-Output 'PHASE174_R3R6R3R2_PYTEST_IMPORT_MODE=importlib'
    Write-Output "PHASE174_R3R6R3R2_FOCUSED_TEST_FILES=$($testFiles.Count)"

    $pytestArgs = @('-q', '--import-mode=importlib', '-p', 'no:cacheprovider')
    if ($DryRun) {
        $pytestArgs += '--collect-only'
        Write-Output 'PHASE174_R3R6R3R2_COLLECTION_START'
    } else {
        Write-Output 'PHASE174_R3R6R3R2_FOCUSED_PYTEST_START'
    }
    $pytestArgs += $testFiles
    python -m pytest @pytestArgs
    if ($LASTEXITCODE -ne 0) {
        if ($DryRun) {
            throw 'R3R2 test collection failed; no production changes made.'
        }
        throw 'R3R2 focused pytest failed; Gate not certified.'
    }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R6R3R2_COLLECTION=PASS'
        Write-Output 'PHASE174_R3R6R3R2_DRY_RUN=PASS'
    } else {
        Write-Output 'PHASE174_R3R6R3R2_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE174_R3R6R3R2_GATE=PASS'
    }
} finally {
    Pop-Location
}
```

## 新規 `verify.py`

```python
"""Verify the previously applied common-renderer patch without applying it again.

The R3R1 implementation succeeded before pytest collection failed.  This
module verifies the exact reviewed function bodies and module imports while
allowing unrelated, non-target local changes.  It never edits production code.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from phase174_r3_r6_r3_common_narrative import patch as original_patch
from phase174_r3_r6_r3r1_scoped_guard_fix import patch as scoped_patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = {
    "phase174_r3_r6_r3_common_narrative/patch.py": (
        "6b79153c208724c179ae6c57fea2fb79507875d3c22f09dc822f25272a1fe01b"
    ),
    "phase174_r3_r6_r3_common_narrative/projection.py": (
        "28f629b1b163ecd55402f0e4d3a71b1d0640b029c59c8a739b5800e3741af995"
    ),
}


def inspect_installed_renderer(root: Path = ROOT) -> tuple[str, ...]:
    """Reject unreviewed target-function/import changes; perform no writes."""
    if not isinstance(root, Path):
        raise TypeError("root must be a Path")
    for relative, expected_hash in SOURCE_SHA256.items():
        source_path = root / relative
        if not source_path.is_file():
            raise ValueError("Missing original reviewed source: " + relative)
        observed_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if observed_hash != expected_hash:
            raise ValueError("Original source has unreviewed changes: " + relative)

    verified = []
    for path, function_name, transform in scoped_patch.TARGETS:
        original_bytes = scoped_patch.git_head_file(root, path)
        if scoped_patch.git_blob_sha(original_bytes) != original_patch.REVIEWED_BLOBS[path]:
            raise ValueError("Unreviewed Git HEAD source: " + path)
        baseline = scoped_patch.normalize_text(original_bytes)
        expected = transform(baseline)
        local_path = root / path
        if not local_path.is_file():
            raise ValueError("Missing applied source: " + path)
        observed = scoped_patch.normalize_text(local_path.read_bytes())
        expected_ast, expected_imports = scoped_patch.statement_ast(
            expected, function_name
        )
        observed_ast, observed_imports = scoped_patch.statement_ast(
            observed, function_name
        )
        if observed_ast != expected_ast or observed_imports != expected_imports:
            raise ValueError(
                "Applied renderer differs from reviewed R3R1 transformation: " + path
            )
        verified.append(path)
    return tuple(verified)


def main() -> int:
    verified = inspect_installed_renderer()
    print("PHASE174_R3R6R3R2_INSTALLED_RENDERER_GUARD=PASS")
    print("PHASE174_R3R6R3R2_VERIFIED_TARGETS=" + str(len(verified)))
    print("PHASE174_R3R6R3R2_PRODUCTION_WRITES=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 `tests/test_r3r2_importmode.py`

```python
"""Regression tests for duplicate basenames during focused pytest collection."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from phase174_r3_r6_r3r2_pytest_importmode_fix import verify


def test_runner_uses_importlib_without_reapplying_production_patch() -> None:
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(
        encoding="utf-8"
    )
    assert "--import-mode=importlib" in script
    assert "--collect-only" in script
    assert "phase172_r5_prior_reference_display/tests/test_projection.py" in script
    assert "phase174_r3_r6_r3_common_narrative/tests/test_projection.py" in script
    assert "phase174_r3_r6_source_extension/tests/test_source.py" in script
    assert "phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py" in script
    assert "scoped_guard_fix.patch --apply" not in script
    assert "common_narrative.patch --apply" not in script


def test_importlib_collects_duplicate_test_projection_modules(tmp_path: Path) -> None:
    left = tmp_path / "left" / "test_projection.py"
    right = tmp_path / "right" / "test_projection.py"
    left.parent.mkdir(parents=True)
    right.parent.mkdir(parents=True)
    left.write_text("def test_left():\n    assert 1 + 1 == 2\n", encoding="utf-8")
    right.write_text("def test_right():\n    assert 2 + 2 == 4\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--import-mode=importlib",
         "-p", "no:cacheprovider", str(left), str(right)],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "2 passed" in result.stdout


def test_inspection_is_read_only_and_has_two_reviewed_targets() -> None:
    assert len(verify.SOURCE_SHA256) == 2
    code = (Path(verify.__file__)).read_text(encoding="utf-8")
    assert "write_bytes(" not in code
    assert "write_text(" not in code
    assert "os.replace(" not in code
    assert "scoped_patch.TARGETS" in code
```

## 新規 `__init__.py`

```python
"""Phase 174 R3-R6-R3R2: read-only pytest collection repair."""
```

## 新規 `tests/__init__.py`

```python
"""Focused tests for Phase 174 R3-R6-R3R2."""
```
