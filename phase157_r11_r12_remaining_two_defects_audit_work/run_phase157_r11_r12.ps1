$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R11-R12 - remaining two defects audit"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$ScriptDir\audit_phase157_r11_r12.py"

if ($LASTEXITCODE -ne 0) {
  throw "R11-R12 audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "pytest: not run"
Write-Host "Full repository pytest remains deferred until Phase157 closure."
