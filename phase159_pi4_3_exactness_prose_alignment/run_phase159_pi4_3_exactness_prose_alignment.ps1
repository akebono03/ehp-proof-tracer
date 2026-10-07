$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 exactness prose alignment"
Write-Host "Align EXACTNESS_TO_KERNEL with existing exactness prose"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Apply minimal generic prose alignment"
python "$PackageDir\apply_phase159_pi4_3_exactness_prose_alignment.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Run Phase 159 pi_4^3 exactness focused tests"
python -m pytest -q `
  ".\tests\test_phase159_pi4_3_exactness_reason_unification.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run existing exactness-to-map-property regression"
python -m pytest -q `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Run pi_4^3 exactness bridge regression"
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
