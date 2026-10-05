$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

function Assert-LastExitCode {
  param(
    [string]$Label
  )

  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5 closure repair1 - stale R5-5a expectation removal"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing R5-5a test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/3] Run current-contract closure tests"
python -m pytest `
  ".\phase158_r5_5_closure_repair1_stale_r5_5a_expectation_removal\test_phase158_r5_5_closure_repair1.py" `
  -q
Assert-LastExitCode "current-contract closure tests"

Write-Host ""
Write-Host "[2/3] Run R5-5b generic-order and Web verification tests"
python -m pytest `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  ".\phase158_r5_5b_repair1v_web_verification_fix\test_phase158_r5_5b_repair1v_web_verification.py" `
  -q
Assert-LastExitCode "R5-5b focused tests"

Write-Host ""
Write-Host "[3/3] Run current-corpus closure cross-check"
python `
  ".\phase158_r5_5_closure_repair1_stale_r5_5a_expectation_removal\audit_phase158_r5_5_closure.py"
Assert-LastExitCode "closure cross-check"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5 closure repair1 verification complete"
Write-Host "Historical R5-5a defect-detection tests were not re-run."
Write-Host "No production code was changed."
Write-Host "Repository-wide pytest was NOT run."
Write-Host "=============================================================="
