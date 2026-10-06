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
Write-Host "Phase 159 R1-7c R3 repair4 - Reference component pruning"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/5] Apply minimal repair4 production change and focused test"
python ".\phase159_r1_7c_r3_repair4_reference_component_pruning\apply_phase159_r1_7c_r3_repair4.py"
Assert-LastExitCode "repair4 apply"

Write-Host ""
Write-Host "[2/5] Run repair4 focused tests"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r3_repair4_reference_component_pruning.py" `
  -q
Assert-LastExitCode "repair4 focused tests"

Write-Host ""
Write-Host "[3/5] Re-run R3 focused tests"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py" `
  -q
Assert-LastExitCode "R3 focused tests"

Write-Host ""
Write-Host "[4/5] Run directly affected regressions"
$RegressionTests = @(
  ".\tests\test_phase75_pi11_4_zero.py",
  ".\tests\test_phase158_r5_5b_public_generic_order_route.py"
)

if (Test-Path ".\tests\test_phase157_r5_r6_53_bracket_definition_reference.py") {
  $RegressionTests += ".\tests\test_phase157_r5_r6_53_bracket_definition_reference.py"
}

python -m pytest @RegressionTests -q
Assert-LastExitCode "directly affected regressions"

Write-Host ""
Write-Host "[5/5] Audit pi_11^4 public Narrative"
python ".\phase159_r1_7c_r3_repair4_reference_component_pruning\audit_phase159_r1_7c_r3_repair4.py"
Assert-LastExitCode "repair4 audit"

Write-Host ""
Write-Host "Phase 159 R1-7c R3 repair4 verification completed."
Write-Host "Repository-wide pytest was intentionally NOT run."
