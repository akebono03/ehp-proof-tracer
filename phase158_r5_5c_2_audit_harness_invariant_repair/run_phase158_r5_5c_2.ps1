$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PhaseDir

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5c-2 - audit-harness invariant repair"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Run lightweight revised-harness tests"
python -m pytest `
  ".\phase158_r5_5c_2_audit_harness_invariant_repair\test_phase158_r5_5c_2_audit_harness.py" `
  -q

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run revised current-corpus equation-chain audit"
python `
  ".\phase158_r5_5c_2_audit_harness_invariant_repair\audit_phase158_r5_5c_2.py"

if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5c-2 audit complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="
