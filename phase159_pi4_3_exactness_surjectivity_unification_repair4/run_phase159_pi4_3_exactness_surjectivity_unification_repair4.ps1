$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 exactness-to-surjectivity repair4"
Write-Host "Canonical surjectivity conclusion assertion"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/6] Apply test-only conclusion assertion repair"
python "$PackageDir\apply_phase159_pi4_3_exactness_surjectivity_unification_repair4.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/6] Run connector normalization focused tests"
python -m pytest -q `
  ".\tests\test_phase159_exactness_connector_normalization.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/6] Run surjectivity focused tests"
python -m pytest -q `
  ".\tests\test_phase159_pi4_3_exactness_surjectivity_unification.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Re-run pi_4^3 kernel exactness prose tests"
python -m pytest -q `
  ".\tests\test_phase159_pi4_3_exactness_reason_unification.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Re-run Phase 150 exactness-to-map-property regression"
python -m pytest -q `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Re-run Phase 50 pi_4^3 exactness bridge"
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
