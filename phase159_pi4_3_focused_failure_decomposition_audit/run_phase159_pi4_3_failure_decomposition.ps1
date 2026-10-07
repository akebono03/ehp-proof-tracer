$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 focused failure decomposition audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/3] Run focused failure decomposition audit"
python "$PackageRoot\audit_phase159_pi4_3_failure_decomposition.py"
if ($LASTEXITCODE -ne 0) {
  throw "Failure decomposition audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/3] Run existing pi_4^3 focused regression"
python -m pytest `
  tests/test_phase50_pi4_3_exactness_bridge.py `
  tests/test_phase50_pi4_3_finite_cyclic.py `
  tests/test_phase50_eta_family_notation.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "Focused regression failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/3] Show audit summary"
Get-Content `
  "$PackageRoot\audit_output\summary.txt" `
  -Encoding UTF8

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 focused audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
