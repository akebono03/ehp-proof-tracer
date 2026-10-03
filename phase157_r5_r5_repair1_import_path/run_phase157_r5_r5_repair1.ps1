$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R5-R5 repair1 - audit import path correction"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageDir\apply_phase157_r5_r5_repair1.py"

Write-Host ""
Write-Host "Re-running the same R5-R5 audit:"
Write-Host ""

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase157_r5_r5_112_group_cross_audit\run_phase157_r5_r5.ps1"

exit $LASTEXITCODE
