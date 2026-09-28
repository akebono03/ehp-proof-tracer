$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R15"
Write-Host "Generic calculation ownership + prerequisite frontier repair"
Write-Host "=============================================================="

python (Join-Path $PatchRoot "apply_phase144_6_final_regression_repair_r15.py")
if ($LASTEXITCODE -ne 0) {
  throw "R15 production repair failed."
}

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "Running six previously failing focused tests..."

  pytest -q `
    ".\tests\test_phase143_57c_step_derivation_connector.py::test_phase143_57c_pi6_3_first_local_derivation_is_grouped" `
    ".\tests\test_phase143_57c_step_derivation_connector.py::test_phase143_57c_pi6_3_second_local_derivation_is_grouped" `
    ".\tests\test_phase143_57c_step_derivation_connector.py::test_phase143_57c_pi6_3_has_two_step_derivation_connectors" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi8_5_direct_premise_is_not_left_at_argument_start" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi6_3_keeps_local_calculation_derivation" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi6_3_does_not_duplicate_order_premises"

  if ($LASTEXITCODE -ne 0) {
    throw "R15 focused six-test regression failed."
  }

  Write-Host ""
  Write-Host "Running complete directly related test files..."

  pytest -q `
    ".\tests\test_phase143_57c_step_derivation_connector.py" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R15 related regression files failed."
  }

  Write-Host ""
  Write-Host "R15 focused regression: PASS"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($CreatedMarker) {
    Remove-Item -Path $Marker -Force -ErrorAction SilentlyContinue
  }
}
