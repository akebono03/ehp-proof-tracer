$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R11-R7 repair1"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "Applying repair1 to the partially-applied R11-R7 state..."
python "$ScriptDir\apply_phase157_r11_r7_repair1.py"

if ($LASTEXITCODE -ne 0) {
  throw "R11-R7 repair1 patch failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Focused pytest:"
python -m pytest `
  tests/test_phase157_r11_reference_reason_punctuation.py `
  tests/test_phase157_r11_proof_body_relevance.py `
  tests/test_phase157_r5_r9_fixed_definition_body_suppression.py `
  tests/test_phase157_r5_r10_reference_proof_boundary_qed.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "R11-R7 repair1 focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Full repository pytest is NOT run here."
Write-Host "It remains deferred until Phase157 closure."
