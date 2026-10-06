$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$PreviousPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = "$RepoRoot;$PreviousPythonPath"
}

try {
  Write-Host "=============================================================="
  Write-Host "Phase 159 R1-7c R4 repair9 fix8"
  Write-Host "fix7 test expectation correction"
  Write-Host "=============================================================="
  Write-Host "Repository root: $RepoRoot"
  Write-Host "Production changes: none"
  Write-Host ""

  Write-Host "[1/5] Syntax compile current fix7 production"
  python -m py_compile `
    ".\toda_literature_statement_boundary.py" `
    ".\toda_group_proof_narrative_references.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Syntax compile failed."
  }

  Write-Host ""
  Write-Host "[2/5] Corrected fix7 focused tests"
  python -m pytest -q `
    ".\phase159_r1_7c_r4_repair9_fix8_fix7_test_expectation\test_phase159_r1_7c_r4_repair9_fix8.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Corrected fix7 focused tests failed."
  }

  Write-Host ""
  Write-Host "[3/5] Existing boundary and inference tests"
  python -m pytest -q `
    ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py" `
    ".\tests\test_phase157_r4_r2_boundary_catalog.py" `
    ".\tests\test_phase156_r5_repair4_bridge_reference_inference.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Existing boundary/inference tests failed."
  }

  Write-Host ""
  Write-Host "[4/5] Repair9 focused regressions"
  python -m pytest -q `
    ".\phase159_r1_7c_r4_repair9_fix5_stale_expectation_repair\test_phase159_r1_7c_r4_repair9_fix5.py" `
    ".\tests\test_phase157_r20_repair30_final_reflexive_suppression.py" `
    ".\tests\test_phase158_r5_5b_public_generic_order_route.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Repair9 regression tests failed."
  }

  Write-Host ""
  Write-Host "[5/5] Registration audit"
  python ".\phase159_r1_7c_r4_repair9_fix8_fix7_test_expectation\audit_phase159_r1_7c_r4_repair9_fix8.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Registration audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair9 fix8 verification completed."
  Write-Host "Production code was NOT changed by fix8."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
