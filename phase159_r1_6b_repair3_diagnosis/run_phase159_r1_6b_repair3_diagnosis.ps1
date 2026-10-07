$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-6b repair3 diagnosis"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host ""

python ".\phase159_r1_6b_repair3_diagnosis\diagnose_phase159_r1_6b_repair3.py"
if ($LASTEXITCODE -ne 0) {
  throw "diagnosis failed"
}
