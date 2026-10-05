$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5d - generic public sequence cross-audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Run lightweight audit-harness tests"
python -m pytest `
  ".\phase158_r5_5d_generic_public_sequence_cross_audit\test_phase158_r5_5d.py" `
  -q

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run current-corpus generic public sequence cross-audit"
python `
  ".\phase158_r5_5d_generic_public_sequence_cross_audit\audit_phase158_r5_5d.py"

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5d audit complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="
