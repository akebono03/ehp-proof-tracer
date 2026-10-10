$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $ProjectRoot 'unified_statement_registry.py'))) {
  throw 'Run this script from the EHP Proof Tracer project root after Phase 163 R2 and R3 installation.'
}
if (-not (Test-Path (Join-Path $ProjectRoot 'phase163_r3_registry_validation.py'))) {
  throw 'Phase 163 R3 module is not installed in this directory.'
}
Copy-Item (Join-Path $PackageRoot 'phase163_r4_registry_bridge.py') (Join-Path $ProjectRoot 'phase163_r4_registry_bridge.py') -Force
Copy-Item (Join-Path $PackageRoot 'audit_phase163_r4.py') (Join-Path $ProjectRoot 'audit_phase163_r4.py') -Force
Copy-Item (Join-Path $PackageRoot 'tests\test_phase163_r4_registry_bridge.py') (Join-Path $ProjectRoot 'tests\test_phase163_r4_registry_bridge.py') -Force
python -m pytest -q tests/test_phase163_r2_unified_registry.py tests/test_phase163_r3_registry_validation.py tests/test_phase163_r4_registry_bridge.py
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
python audit_phase163_r4.py
if ($LASTEXITCODE -ne 0) { throw 'Inventory audit failed' }
Write-Host 'Phase 163 R4 partial migration focused tests complete. Full suite not run.'
