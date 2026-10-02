$ErrorActionPreference = "Stop"

$OutputDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $OutputDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 155 canonical regression"
Write-Host "=============================================================="
Write-Host "This executes the canonical regression set."
Write-Host "This can be HEAVY."
Write-Host ""

python `
  "$OutputDir\run_phase155_canonical_regression.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155 canonical regression failed."
}
