$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 exactness-to-surjectivity repair1"
Write-Host "Normalize focused visibility expectation"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/5] Apply test-only repair"
python "$PackageDir\apply_phase159_pi4_3_exactness_surjectivity_unification_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/5] Run surjectivity focused tests"
python -m pytest -q `
  ".\tests\test_phase159_pi4_3_exactness_surjectivity_unification.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/5] Re-run pi_4^3 exactness prose tests"
python -m pytest -q `
  ".\tests\test_phase159_pi4_3_exactness_reason_unification.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/5] Re-run existing exactness-to-map-property regression"
python -m pytest -q `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/5] Re-run Phase 50 pi_4^3 exactness bridge"
python -m pytest -q `
  ".\tests\test_phase50_pi4_3_exactness_bridge.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Focused verification completed successfully."
Write-Host "Repository-wide tests are intentionally not run."
Write-Host "=============================================================="
