$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$PatchRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$Created=$false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R23"
Write-Host "Phase143-61b-R stale connector expectation repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

python (Join-Path $PatchRoot "apply_phase144_6_final_regression_repair_r23.py")
if ($LASTEXITCODE -ne 0) { throw "R23 apply failed." }

if (-not (Test-Path $Marker)) {
  New-Item $Marker -ItemType File -Force | Out-Null
  $Created=$true
}
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "Running R22/R23 directly related regression files..."
  pytest -q `
    ".\tests\test_phase143_57c_step_derivation_connector.py" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py" `
    ".\tests\test_phase143_61b_r_semantic_suppression_priority.py" `
    ".\tests\test_phase144_5_generic_definition_order_equations.py"
  if ($LASTEXITCODE -ne 0) { throw "R23 related regression failed." }

  Write-Host ""
  Write-Host "R23 related regression: PASS"
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($Created) { Remove-Item $Marker -Force -ErrorAction SilentlyContinue }
}
