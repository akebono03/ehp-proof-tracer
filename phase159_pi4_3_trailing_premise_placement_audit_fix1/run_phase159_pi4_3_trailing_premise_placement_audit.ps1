$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 trailing premise placement audit fix1"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/2] Compile audit script"
python -m py_compile `
  "$ScriptDir\audit_phase159_pi4_3_trailing_premise_placement.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run audit"
python "$ScriptDir\audit_phase159_pi4_3_trailing_premise_placement.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Audit output:"
Write-Host "$ScriptDir\phase159_pi4_3_trailing_premise_placement_audit.txt"
