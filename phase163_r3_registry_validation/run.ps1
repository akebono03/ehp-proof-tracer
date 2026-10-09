$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = $PSScriptRoot
if (-not (Test-Path (Join-Path $ProjectRoot 'unified_statement_registry.py'))) {
  throw 'Phase 163 R2 module is missing. Apply R2 first.'
}
if (-not (Test-Path (Join-Path $ProjectRoot 'tests\test_phase163_r2_unified_registry.py'))) {
  throw 'Phase 163 R2 tests are missing. Apply R2 first.'
}
Copy-Item (Join-Path $PackageRoot 'phase163_r3_registry_validation.py') (Join-Path $ProjectRoot 'phase163_r3_registry_validation.py') -ErrorAction Stop
Copy-Item (Join-Path $PackageRoot 'tests\test_phase163_r3_registry_validation.py') (Join-Path $ProjectRoot 'tests\test_phase163_r3_registry_validation.py') -ErrorAction Stop
python -m pytest -q tests/test_phase163_r2_unified_registry.py tests/test_phase163_r3_registry_validation.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'Phase 163 R3 focused tests complete. Full suite not run.'
