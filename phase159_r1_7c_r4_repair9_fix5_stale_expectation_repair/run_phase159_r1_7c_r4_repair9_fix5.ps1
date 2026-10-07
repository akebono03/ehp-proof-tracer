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
  Write-Host "Phase 159 R1-7c R4 repair9 fix5"
  Write-Host "stale expectation repair only"
  Write-Host "=============================================================="
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/5] Apply test-only stale expectation repair"
  python ".\phase159_r1_7c_r4_repair9_fix5_stale_expectation_repair\apply_phase159_r1_7c_r4_repair9_fix5.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Test-only repair failed."
  }

  Write-Host ""
  Write-Host "[2/5] Targeted audit"
  python ".\phase159_r1_7c_r4_repair9_fix5_stale_expectation_repair\audit_phase159_r1_7c_r4_repair9_fix5.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Targeted audit failed."
  }

  Write-Host ""
  Write-Host "[3/5] repair9 focused tests"
  python -m pytest -q `
    ".\phase159_r1_7c_r4_repair9_fix5_stale_expectation_repair\test_phase159_r1_7c_r4_repair9_fix5.py" `
    ".\tests\test_phase157_r20_repair30_final_reflexive_suppression.py"
  if ($LASTEXITCODE -ne 0) {
    throw "repair9 focused tests failed."
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
  python ".\phase159_r1_7c_r4_repair9_fix5_stale_expectation_repair\audit_phase159_r1_7c_r4_repair9_fix5.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Final targeted audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair9 fix5 verification completed."
  Write-Host "Production code changes in fix5: none."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
