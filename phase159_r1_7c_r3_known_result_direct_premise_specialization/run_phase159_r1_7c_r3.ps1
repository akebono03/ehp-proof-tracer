$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

function Assert-LastExitCode {
  param(
    [string]$Label
  )

  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R3 - known-result direct-premise specialization"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply minimal R3 production change and focused test"
python ".\phase159_r1_7c_r3_known_result_direct_premise_specialization\apply_phase159_r1_7c_r3.py"
Assert-LastExitCode "apply"

Write-Host ""
Write-Host "[2/4] Run new R3 focused tests"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py" `
  -q
Assert-LastExitCode "R3 focused tests"

Write-Host ""
Write-Host "[3/4] Run directly affected structural regressions"
python -m pytest `
  ".\tests\test_phase75_pi11_4_zero.py" `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  -q
Assert-LastExitCode "directly affected regressions"

Write-Host ""
Write-Host "[4/4] Write pi_11^4 public Narrative audit output"
python ".\phase159_r1_7c_r3_known_result_direct_premise_specialization\audit_phase159_r1_7c_r3.py"
Assert-LastExitCode "R3 audit"

Write-Host ""
Write-Host "Phase 159 R1-7c R3 focused verification completed."
Write-Host "Repository-wide pytest was intentionally NOT run."
