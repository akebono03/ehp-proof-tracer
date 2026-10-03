$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R11-R1 repair1 - proof body relevance audit"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""
Write-Host "Working tree:"
git status --short
Write-Host ""

Write-Host "Running R11-R1 repair1 audit..."
python "$ScriptDir\audit_phase157_r11_r1_repair1.py"

if ($LASTEXITCODE -ne 0) {
  throw "R11-R1 repair1 audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "R11-R1 repair1 audit completed."
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "pytest: not run in this audit step"
Write-Host "Full repository pytest remains deferred until Phase157 closure."
