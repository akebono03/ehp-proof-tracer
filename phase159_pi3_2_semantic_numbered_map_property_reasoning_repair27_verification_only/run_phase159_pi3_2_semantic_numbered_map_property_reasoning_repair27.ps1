param()

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 repair27 verification only"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/2] Run focused regression tests"
python -m pytest -q `
  ".\tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py" `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"

if ($LASTEXITCODE -ne 0) {
  throw "focused pytest failed"
}

Write-Host ""
Write-Host "[2/2] Render and verify pi_3^2 public narrative"
python `
  ".\phase159_pi3_2_semantic_numbered_map_property_reasoning_repair27_verification_only\verify_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair27.py"

if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 verification failed"
}

Write-Host ""
Write-Host "Verification complete."
Write-Host "No production files were modified."
Write-Host "Repository-wide pytest was intentionally NOT run."
