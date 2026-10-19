$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$target = Join-Path $root 'phase165_r6_closure_audit\resumable_full_pytest.py'
$source = Join-Path $PSScriptRoot 'resumable_full_pytest.py'
if (-not (Test-Path (Join-Path $root 'phase165_r52_r4_flask_bridge.py'))) { throw 'Run from repository root' }
if (-not (Test-Path $target)) { throw "Missing runner: $target" }
$old = Get-Content $target -Raw -Encoding UTF8
if (-not $old.Contains('recover_successful_batch') -or -not $old.Contains('PHASE 165 AUDITED SCOPE')) { throw 'Runner does not match expected audited-scope checkpoint edition; refusing modification' }
if (-not (Test-Path (Join-Path $root 'phase165_r6_audit_results\resumable_full\state.json'))) { throw 'Missing checkpoint state; refusing modification' }
$backupDir = Join-Path $root 'phase165_r6_audit_results\runner_backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$backup = Join-Path $backupDir ('resumable_full_pytest_before_continue_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.py')
Copy-Item -LiteralPath $target -Destination $backup
& python -m pytest -q -o addopts= (Join-Path $PSScriptRoot 'test_continue.py')
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed; runner not installed.' }
Copy-Item -LiteralPath $source -Destination $target -Force
& python -m py_compile $target
if ($LASTEXITCODE -ne 0) { Copy-Item -LiteralPath $backup -Destination $target -Force; throw 'Syntax check failed; restored backup' }
Write-Host "PATCHED: continue-on-failure mode installed. Backup: $backup"
Write-Host 'No tests or production Python files changed. Existing state and batch logs preserved.'
