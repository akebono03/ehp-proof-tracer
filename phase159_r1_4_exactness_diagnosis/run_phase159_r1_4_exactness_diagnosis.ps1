$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-4 exactness diagnosis"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host ""

python ".\phase159_r1_4_exactness_diagnosis\diagnose_phase159_r1_4_exactness.py"
if ($LASTEXITCODE -ne 0) {
  throw "exactness diagnosis failed"
}
