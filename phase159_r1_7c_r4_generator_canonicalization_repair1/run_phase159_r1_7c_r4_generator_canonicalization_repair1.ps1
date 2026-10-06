$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 generator canonicalization repair1"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/5] Apply repair1"
python ".\phase159_r1_7c_r4_generator_canonicalization_repair1\apply_phase159_r1_7c_r4_generator_canonicalization_repair1.py"

Write-Host ""
Write-Host "[2/5] Run new focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_generator_canonicalization_repair1.py" `
  -q

Write-Host ""
Write-Host "[3/5] Run generic eta normalization regression"
python -m pytest `
  ".\tests\test_phase143_3_generic_eta_normalization.py" `
  -q

Write-Host ""
Write-Host "[4/5] Run Proposition 5.3 integration regression"
python -m pytest `
  ".\tests\test_phase59_prop53_integration.py" `
  -q

Write-Host ""
Write-Host "[5/5] Run pi6^3 generic dependency regression"
python -m pytest `
  ".\tests\test_phase157_r20_generic_dependency_rendering.py" `
  -q

Write-Host ""
Write-Host "=============================================================="
Write-Host "Repair1 focused verification complete"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
