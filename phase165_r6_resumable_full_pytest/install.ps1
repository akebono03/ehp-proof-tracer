$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path '.\phase165_r6_closure_audit\run.ps1')) { throw 'Run from ehp_proof repository root.' }
$dest = Join-Path $root 'phase165_r6_closure_audit'
$backup = Join-Path $root 'phase165_r6_audit_results\runner_backup'
New-Item -ItemType Directory -Force -Path $backup | Out-Null
$old = Join-Path $dest 'run.ps1'
$backupFile = Join-Path $backup ('run_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.ps1')
Copy-Item $old $backupFile
Copy-Item (Join-Path $PSScriptRoot 'run.ps1') $old -Force
Copy-Item (Join-Path $PSScriptRoot 'resumable_full_pytest.py') (Join-Path $dest 'resumable_full_pytest.py') -Force
Write-Host "INSTALLED. Prior run.ps1 backup: $backupFile"
Write-Host 'To run final Phase 165 tests: powershell -ExecutionPolicy Bypass -File .\phase165_r6_closure_audit\run.ps1'
Write-Host 'Use Ctrl+C to interrupt. Run the same command to resume completed batches.'
