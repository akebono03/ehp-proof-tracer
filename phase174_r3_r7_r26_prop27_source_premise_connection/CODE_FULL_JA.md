# R26R1 変更・追加コード全文

## `run.ps1`（既存ファイル全体を置換）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& python -B -m phase174_r3_r7_r26_prop27_source_premise_connection.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R26 Source Guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R26_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}
& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_bridge.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_audit.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_run_import_mode.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_rule.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_lineage.py `
  phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py `
  tests/test_phase50_prop27_theorem_semantics.py
if ($LASTEXITCODE -ne 0) { throw 'R26 focused pytest failed' }
Write-Output 'PHASE174_R3R7R26_RUN=PASS'
Write-Output '(END)'
```

## `tests/test_run_import_mode.py`（新規追加、既存 `tests/test_audit.py` の隣）

```python
from pathlib import Path

RUN_SCRIPT = Path(__file__).resolve().parents[1] / "run.ps1"

def test_focused_pytest_uses_importlib_mode():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert "& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider" in content

def test_both_conflicting_test_audit_modules_remain_selected():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert "phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py" in content
    assert "phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_audit.py" in content

def test_source_guard_still_precedes_pytest():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert content.index("phase174_r3_r7_r26_prop27_source_premise_connection.audit --dry-run") < content.index("& python -B -m pytest")
    assert "if ($LASTEXITCODE -ne 0) { throw 'R26 Source Guard failed' }" in content

def test_full_suite_not_invoked():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert "-p no:cacheprovider" in content
    assert "tests/test_phase50_prop27_theorem_semantics.py" in content
```

その他の Python クラス・関数・import は変更していません。
