$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -X utf8 (Join-Path $PSScriptRoot 'retire.py')
    if ($LASTEXITCODE -ne 0) { throw 'Two-test retirement failed; full suite has not been rerun.' }
    Write-Host 'Archived both missing-fixture historical tests. Resume full pytest with:'
    Write-Host 'powershell -ExecutionPolicy Bypass -File .\phase165_r6_closure_audit\run.ps1'
} finally {
    Pop-Location
}
