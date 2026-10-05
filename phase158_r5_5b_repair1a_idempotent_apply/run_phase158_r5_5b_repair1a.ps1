$ErrorActionPreference = "Stop"

function Assert-LastExitCode {
  param(
    [string]$Label
  )

  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE"
  }
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b repair1a - idempotent apply"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/5] Apply repair1a"
python `
  ".\phase158_r5_5b_repair1a_idempotent_apply\apply_phase158_r5_5b_repair1a.py"
Assert-LastExitCode "apply repair1a"

Write-Host ""
Write-Host "[2/5] Run R5-5b focused ordering tests"
python -m pytest `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  -q
Assert-LastExitCode "R5-5b focused ordering tests"

Write-Host ""
Write-Host "[3/5] Run existing local-body ordering regression"
python -m pytest `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
  -q
Assert-LastExitCode "Phase 149 local-body ordering regression"

Write-Host ""
Write-Host "[4/5] Run directly affected route-contract tests"
python -m pytest `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py" `
  ".\tests\test_phase150_rc4_7d_3_public_narrative_generic_route.py" `
  -q
Assert-LastExitCode "directly affected route-contract tests"

Write-Host ""
Write-Host "[5/5] Show actual Web depth=2 proof bodies"
python `
  ".\phase158_r5_5b_repair1a_idempotent_apply\show_phase158_r5_5b_repair1a_web_body.py"
Assert-LastExitCode "Web proof-body check"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b repair1a focused verification complete"
Write-Host "Repository-wide pytest was NOT run."
Write-Host "=============================================================="
