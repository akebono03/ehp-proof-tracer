$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - public map-property prose dedup repair9"
Write-Host "Deduplicate exactness-qualified injective/surjective prose"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/9] Apply public map-property prose dedup repair"
python "$PackageDir\apply_phase159_public_map_property_prose_dedup_repair9.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[2/9] Run public map-property prose normalizer tests"
python -m pytest -q ".\tests\test_phase159_public_map_property_prose_normalization.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[3/9] Run final public Narrative dedup tests"
python -m pytest -q ".\tests\test_phase159_exactness_map_property_public_dedup.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[4/9] Run four-case generic exactness rule tests"
python -m pytest -q ".\tests\test_phase159_generic_zero_exactness_map_property.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[5/9] Run pi_4^3 surjectivity focused tests"
python -m pytest -q ".\tests\test_phase159_pi4_3_exactness_surjectivity_unification.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[6/9] Run pi_4^3 kernel exactness tests"
python -m pytest -q ".\tests\test_phase159_pi4_3_exactness_reason_unification.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[7/9] Run connector normalization tests"
python -m pytest -q ".\tests\test_phase159_exactness_connector_normalization.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[8/9] Run Phase 150 exactness-to-map-property regression"
python -m pytest -q ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[9/9] Run Phase 50 pi_4^3 exactness bridge regression"
python -m pytest -q ".\tests\test_phase50_pi4_3_exactness_bridge.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Focused verification completed successfully."
Write-Host "Repository-wide tests are intentionally not run."
Write-Host "=============================================================="
