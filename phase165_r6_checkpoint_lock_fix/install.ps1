$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$dest = Join-Path $root 'phase165_r6_closure_audit\resumable_full_pytest.py'
if (-not (Test-Path $dest)) { throw 'Run from repository root after resumable runner install.' }
$before = Get-Content $dest -Raw
if ($before -notmatch 'PHASE 165 AUDITED SCOPE' -or $before -notmatch 'collection_scope.json') { throw 'Unexpected installed runner; refusing patch.' }
$backupDir = Join-Path $root 'phase165_r6_audit_results\runner_backup'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$backup = Join-Path $backupDir ('resumable_full_pytest_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.py')
Copy-Item $dest $backup
Copy-Item (Join-Path $PSScriptRoot 'resumable_full_pytest.py') $dest -Force
& python -m py_compile $dest
if ($LASTEXITCODE -ne 0) { Copy-Item $backup $dest -Force; throw 'Syntax failed; rolled back.' }
Write-Host "PATCHED: Dropbox state replace retry and completed-log recovery. Backup: $backup"
Write-Host 'Existing batch logs and state.json preserved.'
