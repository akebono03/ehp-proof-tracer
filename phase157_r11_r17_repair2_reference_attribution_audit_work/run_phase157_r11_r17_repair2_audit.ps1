$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R11-R17 repair2 pre-audit - Reference attribution"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$ScriptDir\audit_phase157_r11_r17_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "R11-R17 repair2 pre-audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "pytest: not run"
