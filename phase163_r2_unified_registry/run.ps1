$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = $PSScriptRoot
Copy-Item (Join-Path $PackageRoot 'unified_statement_registry.py') (Join-Path $ProjectRoot 'unified_statement_registry.py') -ErrorAction Stop
Copy-Item (Join-Path $PackageRoot 'tests\test_phase163_r2_unified_registry.py') (Join-Path $ProjectRoot 'tests\test_phase163_r2_unified_registry.py') -ErrorAction Stop
python -m pytest -q tests/test_phase163_r2_unified_registry.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'Phase 163 R2 focused tests complete. Full suite not run.'
