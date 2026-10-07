$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 exact-sequence suppression repair1 fix1"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Apply focused-test expectation fix"
python ".\phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1_fix1\apply_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1_fix1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Run pi3^2 focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run existing exactness merge regression"
python -m pytest `
  ".\tests\test_phase157_r20_repair32_exactness_intro_anchor.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Re-run generator canonicalization focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_generator_canonicalization_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Repair1 fix1 focused verification complete"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
