$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R4-R4 - representative output spot-check"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host "Pytest: not run"
Write-Host ""

python "$PackageDir\audit_phase157_r4_r4.py"

Write-Host ""
Write-Host "Phase157-R4-R4 audit execution complete."
Write-Host "This audit is not installed as a permanent test."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."
