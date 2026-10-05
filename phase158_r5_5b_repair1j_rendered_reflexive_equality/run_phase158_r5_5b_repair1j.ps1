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
Write-Host "Phase 158-R5-5b repair1j - rendered reflexive equality"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/7] Apply repair1j"
python `
  ".\phase158_r5_5b_repair1j_rendered_reflexive_equality\apply_phase158_r5_5b_repair1j.py"
Assert-LastExitCode "apply repair1j"

Write-Host ""
Write-Host "[2/7] Run Phase 156 relation-side normalization tests"
python -m pytest `
  ".\tests\test_phase156_r6_repair2_independent_relation_side_normalization.py" `
  -q
Assert-LastExitCode "Phase 156 relation-side normalization"

Write-Host ""
Write-Host "[3/7] Run Phase 157 reflexive-equality suppression tests"
python -m pytest `
  ".\tests\test_phase157_r20_repair28_match_step_level_eta_normalization.py" `
  -q
Assert-LastExitCode "Phase 157 reflexive-equality suppression"

Write-Host ""
Write-Host "[4/7] Run Phase 149 local-body ordering regression"
python -m pytest `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
  -q
Assert-LastExitCode "Phase 149 local-body ordering regression"

Write-Host ""
Write-Host "[5/7] Run R5-5b focused ordering tests"
python -m pytest `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  -q
Assert-LastExitCode "R5-5b focused ordering tests"

Write-Host ""
Write-Host "[6/7] Run directly affected Phase 150 route-contract tests"
python -m pytest `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py" `
  ".\tests\test_phase150_rc4_7d_3_public_narrative_generic_route.py" `
  -q
Assert-LastExitCode "Phase 150 route-contract tests"

Write-Host ""
Write-Host "[7/7] Show actual Web depth=2 proof bodies"
python `
  ".\phase158_r5_5b_repair1j_rendered_reflexive_equality\show_phase158_r5_5b_repair1j_web_body.py"
Assert-LastExitCode "Web proof-body check"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b repair1j focused verification complete"
Write-Host "Repository-wide pytest was NOT run."
Write-Host "=============================================================="
