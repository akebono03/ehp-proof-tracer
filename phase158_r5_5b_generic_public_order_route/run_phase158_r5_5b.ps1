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
Write-Host "Phase 158-R5-5b - generic public ordering route"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply Phase 158-R5-5b"
python `
  ".\phase158_r5_5b_generic_public_order_route\apply_phase158_r5_5b.py"
Assert-LastExitCode "apply Phase 158-R5-5b"

Write-Host ""
Write-Host "[2/4] Run new focused ordering tests"
python -m pytest `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  -q
Assert-LastExitCode "new focused ordering tests"

Write-Host ""
Write-Host "[3/4] Run directly affected route-contract tests"
python -m pytest `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py" `
  ".\tests\test_phase150_rc4_7d_3_public_narrative_generic_route.py" `
  -q
Assert-LastExitCode "directly affected route-contract tests"

Write-Host ""
Write-Host "[4/4] Show actual Web depth=2 excerpts"
python `
  ".\phase158_r5_5b_generic_public_order_route\show_phase158_r5_5b_web_output.py"
Assert-LastExitCode "Web output check"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b focused verification complete"
Write-Host "Repository-wide pytest was NOT run."
Write-Host "=============================================================="
