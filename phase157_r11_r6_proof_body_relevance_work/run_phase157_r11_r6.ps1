$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R11-R6 - proof body relevance implementation"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "Applying R11-R6 patch..."
python "$ScriptDir\apply_phase157_r11_r6.py"

if ($LASTEXITCODE -ne 0) {
  throw "R11-R6 patch failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Focused pytest (lightweight):"
python -m pytest `
  tests/test_phase157_r11_proof_body_relevance.py `
  tests/test_phase157_r5_r9_fixed_definition_body_suppression.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "R11-R6 focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Phase157 R11-R6 focused checks completed."
Write-Host "Full repository pytest is intentionally NOT run here."
Write-Host "It remains deferred until Phase157 closure."
