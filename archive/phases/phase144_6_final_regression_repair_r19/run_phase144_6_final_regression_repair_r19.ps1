$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$PatchRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$Created=$false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R19"
Write-Host "cross-Argument completed-step suppression"
Write-Host "=============================================================="

python (Join-Path $PatchRoot "apply_phase144_6_final_regression_repair_r19.py")
if ($LASTEXITCODE -ne 0) { throw "R19 apply failed." }

if (-not (Test-Path $Marker)) {
  New-Item $Marker -ItemType File -Force | Out-Null
  $Created=$true
}
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "Running the two R18-confirmed duplicate regressions..."
  pytest -q `
    ".\tests\test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi8_5_places_direct_derivation_premises_together" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi6_3_does_not_duplicate_order_premises"
  if ($LASTEXITCODE -ne 0) { throw "R19 duplicate regression failed." }

  Write-Host ""
  Write-Host "Running directly related regression files..."
  pytest -q `
    ".\tests\test_phase143_57c_step_derivation_connector.py" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py" `
    ".\tests\test_phase143_61b_r_semantic_suppression_priority.py" `
    ".\tests\test_phase144_5_generic_definition_order_equations.py"
  if ($LASTEXITCODE -ne 0) { throw "R19 related regression failed." }

  Write-Host ""
  Write-Host "R19 focused regression: PASS"
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($Created) { Remove-Item $Marker -Force -ErrorAction SilentlyContinue }
}
