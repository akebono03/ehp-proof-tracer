$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 exact-sequence suppression repair2 fix4"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/5] Apply whitespace-normalized Phase157 expectation repair"
python ".\phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair2_fix4\apply_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair2_fix4.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/5] Run Phase157 exactness display regression"
python -m pytest `
  ".\tests\test_phase157_r20_repair32_exactness_intro_anchor.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/5] Run pi3^2 focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/5] Run late-prefix helper contract regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_exact_sequence_late_prefix_suppression_repair2.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/5] Re-run generator canonicalization focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_generator_canonicalization_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Repair2 fix4 focused verification complete"
Write-Host "Production code changes: none in fix4"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
