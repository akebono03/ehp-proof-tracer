$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 corrected provenance route audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/3] Run corrected provenance route audit"
python "$PackageRoot\audit_phase159_pi4_3_corrected_provenance_route.py"
if ($LASTEXITCODE -ne 0) {
  throw "Audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/3] Run focused existing regression"
python -m pytest `
  tests/test_phase50_pi4_3_exactness_bridge.py `
  tests/test_phase52_delta_direct_bridge.py `
  tests/test_phase55_prop51_integration.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "Focused regression failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/3] Show summary"
Get-Content `
  "$PackageRoot\audit_output\summary.txt" `
  -Encoding UTF8

Write-Host ""
Write-Host "=============================================================="
Write-Host "Corrected audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
