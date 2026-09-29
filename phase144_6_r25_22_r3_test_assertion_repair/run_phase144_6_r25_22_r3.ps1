$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-22-R3 Focused-Test Assertion Repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Repairing R25-22-R2 HTML LaTeX assertions..."
  python `
    ".\phase144_6_r25_22_r3_test_assertion_repair\repair_phase144_6_r25_22_r3.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22-R3 assertion repair failed."
  }
  Write-Host ""

  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\web_group_proof.py" `
    ".\phase144_6_r25_22_r2_web_numbered_equation_adapter\test_phase144_6_r25_22_r2.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22-R3 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "C. Re-running R25-22-R2 focused Web numbering tests..."
  pytest -q `
    ".\phase144_6_r25_22_r2_web_numbered_equation_adapter\test_phase144_6_r25_22_r2.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22-R3 focused tests failed."
  }
  Write-Host ""

  Write-Host "D. Existing generic equation-numbering regression..."
  pytest -q `
    ".\tests\test_phase144_5_generic_definition_order_equations.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22-R3 equation-numbering regression failed."
  }
  Write-Host ""

  Write-Host "E. Existing Web Narrative formatting regressions..."
  pytest -q `
    ".\tests\test_phase135_1_web_narrative_display_math.py" `
    ".\tests\test_phase135_2_web_narrative_inline_formatting.py" `
    ".\tests\test_phase135_3_web_narrative_readability.py" `
    ".\tests\test_phase132_9_web_group_proof_modes.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22-R3 Web Narrative regressions failed."
  }
  Write-Host ""

  Write-Host "F. Existing generic pi6 production-route regression..."
  pytest -q `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-22-R3 generic pi6 route regression failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-22-R3 checks completed."
  Write-Host "Production changes in R3: none."
  Write-Host "Manual Web check:"
  Write-Host "  pi_6^3 / depth 2 / Narrative"
  Write-Host "  Confirm equation numbers (1), (2), (3), ... are visible."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
