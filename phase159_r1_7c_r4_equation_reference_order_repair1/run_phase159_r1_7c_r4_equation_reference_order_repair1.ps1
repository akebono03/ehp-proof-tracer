$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 equation-reference order repair1"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/7] Apply repair1"
python ".\phase159_r1_7c_r4_equation_reference_order_repair1\apply_phase159_r1_7c_r4_equation_reference_order_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/7] Run equation-reference order focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_equation_reference_order_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/7] Re-run numbered-reasoning focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/7] Re-run map-property prose regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/7] Re-run pi3^2 exact-sequence regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/7] Re-run Phase157 pi6^3 exactness display regression"
python -m pytest `
  ".\tests\test_phase157_r20_repair32_exactness_intro_anchor.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[7/7] Re-run generator canonicalization regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_generator_canonicalization_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Equation-reference order repair1 focused verification complete"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
