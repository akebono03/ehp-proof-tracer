$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-3 repair3 diagnosis - eta2 definition premises"
Write-Host "=============================================================="
Write-Host ""

python ".\phase159_r1_3_repair3_diagnosis\diagnose_phase159_r1_3_repair3.py"
if ($LASTEXITCODE -ne 0) {
  throw "diagnosis failed"
}
