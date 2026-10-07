$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 exact-sequence suppression audit2"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/2] Print pi3^2 / pi6^3 sequence paragraphs before and after merge"
python ".\phase159_r1_7c_r4_exact_sequence_subsequence_suppression_audit2\audit_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_audit2.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Confirm current focused regression state"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py" `
  ".\tests\test_phase157_r20_repair32_exactness_intro_anchor.py" `
  -q

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit2 complete"
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
