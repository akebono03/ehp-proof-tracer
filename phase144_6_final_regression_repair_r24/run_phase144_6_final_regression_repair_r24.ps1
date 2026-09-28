$ErrorActionPreference="Stop"
$ProjectRoot=(Get-Location).Path
$PatchRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker=Join-Path $ProjectRoot "tests\__init__.py"
$Created=$false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R24"
Write-Host "Remaining two final-completion regressions"
Write-Host "=============================================================="

if (-not (Test-Path $Marker)) {
  New-Item $Marker -ItemType File -Force | Out-Null
  $Created=$true
}
$env:PYTHONPATH="$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "A. Inspecting depth=2 Narrative argument boundary..."
  python (Join-Path $PatchRoot "diagnose_phase144_6_r24.py")
  $Diagnosis=$LASTEXITCODE

  if ($Diagnosis -eq 20) {
    throw "Unexpected state: depth=2 already contains establish_definition. R24 will not patch the wrong layer."
  }
  if ($Diagnosis -ne 21) {
    throw "Unexpected R24 diagnosis exit code: $Diagnosis"
  }

  Write-Host ""
  Write-Host "Confirmed: depth=2 presentation omits establish_definition."
  Write-Host "Applying the two minimal repairs..."

  python (Join-Path $PatchRoot "apply_phase144_6_r24_frontier.py")
  if ($LASTEXITCODE -ne 0) { throw "R24 frontier repair failed." }

  python (Join-Path $PatchRoot "apply_phase144_6_r24_cli.py")
  if ($LASTEXITCODE -ne 0) { throw "R24 CLI repair failed." }

  Write-Host ""
  Write-Host "B. Re-running the two failed final-completion tests..."
  pytest -q `
    ".\tests\test_phase144_6_pi6_generic_production_route.py::test_phase144_6_cli_pi6_3_narrative_uses_generic_route" `
    ".\tests\test_phase144_6_r4_supporting_fact_filtering.py::test_phase144_6_r4_hides_internal_supporting_group_facts"
  if ($LASTEXITCODE -ne 0) { throw "R24 two-regression check failed." }

  Write-Host ""
  Write-Host "C. Running directly related regressions..."
  pytest -q `
    ".\tests\test_phase144_6_pi6_generic_production_route.py" `
    ".\tests\test_phase144_6_r4_supporting_fact_filtering.py" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py" `
    ".\tests\test_phase143_61b_r_semantic_suppression_priority.py" `
    ".\tests\test_phase144_5_generic_definition_order_equations.py"
  if ($LASTEXITCODE -ne 0) { throw "R24 related regression failed." }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R24 focused regression: PASS"
  Write-Host "=============================================================="
  Write-Host "No full pytest was run."
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($Created) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
