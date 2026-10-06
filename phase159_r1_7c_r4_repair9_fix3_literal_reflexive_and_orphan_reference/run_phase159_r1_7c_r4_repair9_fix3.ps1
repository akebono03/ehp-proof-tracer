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
  Write-Host "Phase 159 R1-7c R4 repair9 fix3"
  Write-Host "literal reflexive + orphan Reference suppression"
  Write-Host "=============================================================="
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/5] Apply fix3"
  python ".\phase159_r1_7c_r4_repair9_fix3_literal_reflexive_and_orphan_reference\apply_phase159_r1_7c_r4_repair9_fix3.py"
  if ($LASTEXITCODE -ne 0) {
    throw "fix3 apply failed."
  }

  Write-Host ""
  Write-Host "[2/5] Targeted audit"
  python ".\phase159_r1_7c_r4_repair9_fix3_literal_reflexive_and_orphan_reference\audit_phase159_r1_7c_r4_repair9_fix3.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Targeted audit failed."
  }

  Write-Host ""
  Write-Host "[3/5] repair9 fix3 focused tests"
  python -m pytest -q `
    ".\phase159_r1_7c_r4_repair9_fix3_literal_reflexive_and_orphan_reference\test_phase159_r1_7c_r4_repair9_fix3.py" `
    ".\tests\test_phase157_r20_repair30_final_reflexive_suppression.py"
  if ($LASTEXITCODE -ne 0) {
    throw "repair9 fix3 focused tests failed."
  }

  Write-Host ""
  Write-Host "[4/5] Current generic-route contract tests"
  python -m pytest -q `
    ".\tests\test_phase158_r5_5b_public_generic_order_route.py" `
    ".\tests\test_phase157_r20_repair12_map_property_reference_support.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Current generic-route contract tests failed."
  }

  Write-Host ""
  Write-Host "[5/5] Final targeted audit"
  python ".\phase159_r1_7c_r4_repair9_fix3_literal_reflexive_and_orphan_reference\audit_phase159_r1_7c_r4_repair9_fix3.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Final targeted audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair9 fix3 focused verification completed."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "Phase157 pi15 dedicated-renderer tests were NOT used because"
  Write-Host "Phase158 moved pi15_8 to the generic public route."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
