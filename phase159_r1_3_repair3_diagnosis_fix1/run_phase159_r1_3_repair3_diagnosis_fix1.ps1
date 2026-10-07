$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$OldPythonPath = $env:PYTHONPATH
if ([string]::IsNullOrWhiteSpace($OldPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = "$RepoRoot;$OldPythonPath"
}

Write-Host "=============================================================="
Write-Host "Phase 159-R1-3 repair3 diagnosis fix1"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "PYTHONPATH includes repository root."
Write-Host ""

python ".\phase159_r1_3_repair3_diagnosis_fix1\diagnose_phase159_r1_3_repair3.py"
if ($LASTEXITCODE -ne 0) {
  throw "diagnosis failed"
}
