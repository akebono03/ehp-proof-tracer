# Phase 174 R3-R7-R4R1 — 完全変更コード

GitHub `develop` の監査対象 HEAD: `1f3a61d7d6cfc7854e56c4f5c372bf5c71e203df`。変更は `run.ps1` 全体の置換、新規 `tests/test_r4_runner_split.py` の追加です。既存の import、本体クラス・関数、関連テストを変更しません。

## `run.ps1` 全文（置換）

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir '..')).Path
Push-Location $RepoRoot
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # The Phase R4 and Phase R3 test_audit.py files have the same basename.
    # Run each test group in a separate Python process. Keep prepend mode
    # because importlib mode conflicts with existing module/package names.
    $R4Tests = @(
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
    )
    $RegressionTests = @(
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py',
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
        '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
        '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py'
    )
    $FocusedTests = @($R4Tests + $RegressionTests)
    foreach ($TestPath in $FocusedTests) {
        if (-not (Test-Path -LiteralPath $TestPath)) {
            throw "Focused pytest file missing: $TestPath"
        }
    }

    Write-Output 'PHASE174_R3R7R4_FOCUSED_PYTEST_START'
    Write-Output 'PHASE174_R3R7R4_PYTEST_GROUP=R4'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @R4Tests
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R4 own pytest failed: $LASTEXITCODE"
    }
    Write-Output 'PHASE174_R3R7R4_PYTEST_GROUP=REGRESSION'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @RegressionTests
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R4 regression pytest failed: $LASTEXITCODE"
    }
    Write-Output 'PHASE174_R3R7R4_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B '.\phase174_r3_r7_r4_delta_surjectivity_audit\audit.py' --dry-run
    }
    else {
        & python -B '.\phase174_r3_r7_r4_delta_surjectivity_audit\audit.py'
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R4 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
```

## `tests/test_r4_runner_split.py` 全文（新規追加）

配置場所: `phase174_r3_r7_r4_delta_surjectivity_audit/tests/test_r4_runner_split.py`。

```python
"""Focused regression guards for duplicate pytest module names."""
from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys


RUNNER = Path(__file__).resolve().parents[1] / "run.ps1"


def _test_group(source: str, variable_name: str) -> tuple[str, ...]:
    match = re.search(
        r"\$" + re.escape(variable_name) + r"\s*=\s*@\((.*?)\)",
        source,
        flags=re.DOTALL,
    )
    assert match is not None
    return tuple(re.findall(r"'([^']+\.py)'", match.group(1)))


def test_r4_and_r3_duplicate_audit_names_use_independent_processes() -> None:
    source = RUNNER.read_text(encoding="utf-8-sig")
    local = _test_group(source, "R4Tests")
    regression = _test_group(source, "RegressionTests")
    assert any("phase174_r3_r7_r4_delta_surjectivity_audit" in path
               and path.endswith("test_audit.py") for path in local)
    assert any("phase174_r3_r7_r3_ehp_zero_rule" in path
               and path.endswith("test_audit.py") for path in regression)
    assert len(local) == 2
    assert len(regression) == 4
    assert {Path(path).name for path in local}.isdisjoint(
        {Path(path).name for path in regression} - {"test_audit.py"}
    )
    invocations = re.findall(
        r"& python -B -m pytest -q --import-mode=prepend -p no:cacheprovider\s+@(\w+)",
        source,
    )
    assert invocations == ["R4Tests", "RegressionTests"]
    assert "--import-mode=importlib" not in source


def test_runner_preserves_preflight_and_fail_closed_guards() -> None:
    source = RUNNER.read_text(encoding="utf-8-sig")
    assert "foreach ($TestPath in $FocusedTests)" in source
    assert source.count("if ($LASTEXITCODE -ne 0)") == 3
    assert "PHASE174_R3R7R4_FOCUSED_PYTEST=PASS" in source
    assert "audit.py' --dry-run" in source
    assert "audit.py'" in source
    assert "$env:PYTHONPATH = $PreviousPythonPath" in source
    assert "$env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode" in source
    assert "Pop-Location" in source
    assert "pytest -q --import-mode=prepend -p no:cacheprovider" in source
    assert "--all" not in source


def test_duplicate_test_module_basename_fails_together_and_passes_split(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first" / "tests" / "test_audit.py"
    second = tmp_path / "second" / "tests" / "test_audit.py"
    for test_file in (first, second):
        test_file.parent.mkdir(parents=True)
        test_file.write_text(
            "def test_collection_contract():\n    assert 1 + 1 == 2\n",
            encoding="utf-8",
        )
    base = [
        sys.executable, "-B", "-m", "pytest", "-q",
        "--import-mode=prepend", "-p", "no:cacheprovider",
    ]
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    combined = subprocess.run(
        base + [str(first), str(second)],
        cwd=tmp_path, env=environment, text=True,
        capture_output=True, check=False,
    )
    assert combined.returncode != 0
    assert "import file mismatch" in combined.stdout.lower()
    for test_file in (first, second):
        separate = subprocess.run(
            base + [str(test_file)],
            cwd=tmp_path, env=environment, text=True,
            capture_output=True, check=False,
        )
        assert separate.returncode == 0, separate.stdout + separate.stderr
```

## 変更一覧・テスト・完了条件

- 既存の `test_audit.py` 2本を別プロセスで収集。既存テストを削除せず、 `--import-mode=prepend` を維持。
- 修正テスト: `python -B -m pytest -q --import-mode=prepend -p no:cacheprovider phase174_r3_r7_r4_delta_surjectivity_audit/tests/test_r4_runner_split.py`。
- Windows では `run.ps1 -DryRun` PASS 後に `run.ps1` を実行。
- 完了条件: 両グループの限定 pytest、Source Guard、ライブ監査の PASS。数学的な証明完成は条件ではない。
- 次 Phase との境界: R3-R7-R5 の数学的な推論規則や GIVEN は追加しない。全体テストは Phase 174 終了時のみ。
