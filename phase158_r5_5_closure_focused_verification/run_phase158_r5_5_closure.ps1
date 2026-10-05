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
Write-Host "Phase 158-R5-5 closure / focused verification"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Run R5-5a focused audit-contract tests"
python -m pytest `
  ".\phase158_r5_5a_public_depth2_audit_parity_repair\test_phase158_r5_5a.py" `
  -q
Assert-LastExitCode "R5-5a focused tests"

Write-Host ""
Write-Host "[2/4] Run R5-5b generic-order and Web verification tests"
python -m pytest `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  ".\phase158_r5_5b_repair1v_web_verification_fix\test_phase158_r5_5b_repair1v_web_verification.py" `
  -q
Assert-LastExitCode "R5-5b focused tests"

Write-Host ""
Write-Host "[3/4] Run closure-harness lightweight tests"
python -m pytest `
  ".\phase158_r5_5_closure_focused_verification\test_phase158_r5_5_closure.py" `
  -q
Assert-LastExitCode "closure harness tests"

Write-Host ""
Write-Host "[4/4] Run current-corpus closure cross-check"
python `
  ".\phase158_r5_5_closure_focused_verification\audit_phase158_r5_5_closure.py"
Assert-LastExitCode "closure cross-check"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5 closure verification complete"
Write-Host "No production code was changed."
Write-Host "Repository-wide pytest was NOT run."
Write-Host "=============================================================="
