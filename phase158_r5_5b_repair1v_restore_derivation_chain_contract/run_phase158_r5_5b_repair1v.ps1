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
Write-Host "Phase 158-R5-5b repair1v - restore derivation-chain contract"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/9] Apply repair1v"
python `
  ".\phase158_r5_5b_repair1v_restore_derivation_chain_contract\apply_phase158_r5_5b_repair1v.py"
Assert-LastExitCode "apply repair1v"

Write-Host ""
Write-Host "[2/9] Run generic dependency-order tests"
python -m pytest `
  ".\tests\test_phase143_1_generic_proof_order.py" `
  ".\tests\test_phase143_1b_semantic_proof_order.py" `
  -q
Assert-LastExitCode "generic dependency-order tests"

Write-Host ""
Write-Host "[3/9] Run Phase 144 equation-numbering tests"
python -m pytest `
  ".\tests\test_phase144_5_generic_definition_order_equations.py" `
  -q
Assert-LastExitCode "Phase 144 equation-numbering tests"

Write-Host ""
Write-Host "[4/9] Run Phase 149 local-body ordering regression"
python -m pytest `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
  -q
Assert-LastExitCode "Phase 149 local-body ordering"

Write-Host ""
Write-Host "[5/9] Run Phase 156 relation-side normalization"
python -m pytest `
  ".\tests\test_phase156_r6_repair2_independent_relation_side_normalization.py" `
  -q
Assert-LastExitCode "Phase 156 relation-side normalization"

Write-Host ""
Write-Host "[6/9] Run Phase 156 connector/local-order tests"
python -m pytest `
  ".\tests\test_phase156_r6_canonical_connector_local_ordering.py" `
  -q
Assert-LastExitCode "Phase 156 connector/local-order"

Write-Host ""
Write-Host "[7/9] Run Phase 157 cleanup regressions"
python -m pytest `
  ".\tests\test_phase157_r20_repair30_final_reflexive_suppression.py" `
  ".\tests\test_phase157_r20_repair43_dangling_connector_cleanup.py" `
  -q
Assert-LastExitCode "Phase 157 cleanup regressions"

Write-Host ""
Write-Host "[8/9] Run R5-5b public ordering tests"
python -m pytest `
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
  -q
Assert-LastExitCode "R5-5b public ordering tests"

Write-Host ""
Write-Host "[9/9] Show public Web proof bodies"
python `
  ".\phase158_r5_5b_repair1v_restore_derivation_chain_contract\show_phase158_r5_5b_repair1v_web.py"
Assert-LastExitCode "public Web proof bodies"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b repair1v focused verification complete"
Write-Host "Repository-wide pytest was NOT run."
Write-Host "=============================================================="
