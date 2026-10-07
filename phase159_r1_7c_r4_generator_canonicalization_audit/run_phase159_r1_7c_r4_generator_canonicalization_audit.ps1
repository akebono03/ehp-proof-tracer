$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 generator canonicalization audit"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/3] Run generator canonicalization audit"
python ".\phase159_r1_7c_r4_generator_canonicalization_audit\audit_phase159_r1_7c_r4_generator_canonicalization.py"

Write-Host ""
Write-Host "[2/3] Run existing generic eta normalization tests"
python -m pytest `
  ".\tests\test_phase143_3_generic_eta_normalization.py" `
  -q

Write-Host ""
Write-Host "[3/3] Run existing Proposition 5.3 integration tests"
python -m pytest `
  ".\tests\test_phase59_prop53_integration.py" `
  -q

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit complete"
Write-Host "No production files were modified."
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
