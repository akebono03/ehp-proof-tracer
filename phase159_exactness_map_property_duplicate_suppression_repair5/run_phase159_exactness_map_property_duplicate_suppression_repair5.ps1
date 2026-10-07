$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - exactness map-property duplicate suppression repair5"
Write-Host "Function-level test replacement"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/7] Apply idempotent connector repair and replace test functions"
python "$PackageDir\apply_phase159_exactness_map_property_duplicate_suppression_repair5.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[2/7] Run four-case generic rule tests"
python -m pytest -q ".\tests\test_phase159_generic_zero_exactness_map_property.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[3/7] Run pi_4^3 surjectivity focused tests"
python -m pytest -q ".\tests\test_phase159_pi4_3_exactness_surjectivity_unification.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[4/7] Run pi_4^3 kernel exactness tests"
python -m pytest -q ".\tests\test_phase159_pi4_3_exactness_reason_unification.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[5/7] Run connector normalization tests"
python -m pytest -q ".\tests\test_phase159_exactness_connector_normalization.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[6/7] Run Phase 150 exactness-to-map-property regression"
python -m pytest -q ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[7/7] Run Phase 50 pi_4^3 exactness bridge regression"
python -m pytest -q ".\tests\test_phase50_pi4_3_exactness_bridge.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Focused verification completed successfully."
Write-Host "Repository-wide tests are intentionally not run."
Write-Host "=============================================================="
