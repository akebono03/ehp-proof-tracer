$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 exactness reason unification repair1"
Write-Host "Test expectation normalization only"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/3] Apply test-only repair"
python "$PackageDir\apply_phase159_pi4_3_exactness_reason_unification_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/3] Run focused Phase 159 test"
python -m pytest -q `
  ".\tests\test_phase159_pi4_3_exactness_reason_unification.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/3] Run directly related regression tests"
python -m pytest -q `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
  ".\tests\test_phase50_pi4_3_exactness_bridge.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Focused verification completed successfully."
Write-Host "Repository-wide tests are intentionally not run."
Write-Host "=============================================================="
