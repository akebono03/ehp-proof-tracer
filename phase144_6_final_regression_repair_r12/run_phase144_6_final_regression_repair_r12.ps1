$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R12"
Write-Host "ProofStep-level non-EXACTNESS dedup"
Write-Host "=============================================================="

python (Join-Path $PatchRoot "apply_phase144_6_final_regression_repair_r12.py")
if ($LASTEXITCODE -ne 0) { throw "R12 apply failed." }

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}
$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "Running R11 failing Narrative regressions..."
  pytest -q `
    "tests/test_phase143_57c_step_derivation_connector.py::test_phase143_57c_pi6_3_first_local_derivation_is_grouped" `
    "tests/test_phase143_57c_step_derivation_connector.py::test_phase143_57c_pi6_3_second_local_derivation_is_grouped" `
    "tests/test_phase143_57c_step_derivation_connector.py::test_phase143_57c_pi6_3_has_two_step_derivation_connectors" `
    "tests/test_phase143_58a_negative_scalar_sum.py::test_phase143_58a_pi6_3_narrative_normalizes_negative_scalar_sum" `
    "tests/test_phase143_59b_group_structure_duplicate_suppression.py::test_phase143_59b_pi6_3_narrative_remains_available" `
    "tests/test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi8_5_direct_premise_is_not_left_at_argument_start" `
    "tests/test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi6_3_keeps_local_calculation_derivation" `
    "tests/test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi6_3_does_not_duplicate_order_premises" `
    "tests/test_phase143_61b_r_semantic_suppression_priority.py::test_phase143_61b_r_keeps_pi6_3_local_connector"
  if ($LASTEXITCODE -ne 0) { throw "R12 focused Narrative regressions failed." }

  Write-Host ""
  Write-Host "Running R10/R11 boundary regressions..."
  pytest -q `
    "tests/test_phase143_51b_aggregate_statement_prose.py" `
    "tests/test_phase143_57c_step_derivation_connector.py" `
    "tests/test_phase143_61b_direct_premise_narrative.py"
  if ($LASTEXITCODE -ne 0) { throw "R12 boundary regressions failed." }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 Final Regression Repair R12 focused tests: PASS"
  Write-Host "Full suite intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
