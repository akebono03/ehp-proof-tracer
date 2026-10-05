$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R5-R1 - 112-group Literature Statement Boundary audit"
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
Write-Host "Full Narrative rendering: not used"
Write-Host ""

python "$PackageDir\audit_phase157_r5_r1.py"

Write-Host ""
Write-Host "Phase157-R5-R1 audit complete."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."
