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
Write-Host "Phase 158-R5-5b repair1o - contribution rendered reflexive"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/7] Apply repair1o"
python `
  ".\phase158_r5_5b_repair1o_contribution_rendered_reflexive\apply_phase158_r5_5b_repair1o.py"
Assert-LastExitCode "apply repair1o"

Write-Host ""
Write-Host "[2/7] Run Phase 157 final reflexive-suppression tests"
python -m pytest `
  ".\tests\test_phase157_r20_repair30_final_reflexive_suppression.py" `
  -q
Assert-LastExitCode "Phase 157 final reflexive suppression"

Write-Host ""
Write-Host "[3/7] Run Phase 156 relation-side normalization tests"
python -m pytest `
  ".\tests\test_phase156_r6_repair2_independent_relation_side_normalization.py" `
  -q
Assert-LastExitCode "Phase 156 relation-side normalization"

Write-Host ""
Write-Host "[4/7] Run Phase 156 canonical connector/local-order tests"
python -m pytest `
  ".\tests\test_phase156_r6_canonical_connector_local_ordering.py" `
  -q
Assert-LastExitCode "Phase 156 canonical connector/local-order"

Write-Host ""
Write-Host "[5/7] Run Phase 149 local-body ordering regression"
python -m pytest `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
  -q
Assert-LastExitCode "Phase 149 local-body ordering regression"

Write-Host ""
Write-Host "[6/7] Run R5-5b focused ordering tests"
python -m pytest `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  -q
Assert-LastExitCode "R5-5b focused ordering tests"

Write-Host ""
Write-Host "[7/7] Show pi6 chain surfaces"
python `
  ".\phase158_r5_5b_repair1o_contribution_rendered_reflexive\show_phase158_r5_5b_repair1o_chain.py"
Assert-LastExitCode "pi6 chain surface check"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b repair1o focused verification complete"
Write-Host "Repository-wide pytest was NOT run."
Write-Host "=============================================================="
