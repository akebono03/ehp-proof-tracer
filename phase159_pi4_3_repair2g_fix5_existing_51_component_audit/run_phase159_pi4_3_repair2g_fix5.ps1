$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2g fix5 audit"
Write-Host "Existing (5.1) component provenance audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Audit pi_3^2 and pi_4^3 (5.1) component flow"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix5.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair2g fix5 audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/2] Run current repair2g focused tests for failure inventory"
python -m pytest `
  tests/test_phase159_pi4_3_repair2g_reference_policy.py `
  -q
$FocusedExit = $LASTEXITCODE

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair2g fix5 audit complete"
Write-Host "Focused pytest exit code: $FocusedExit"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="

exit 0
