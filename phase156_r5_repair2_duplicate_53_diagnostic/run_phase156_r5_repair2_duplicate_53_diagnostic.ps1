$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 repair2 - duplicate (5.3) diagnostic"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python -m `
  phase156_r5_repair2_duplicate_53_diagnostic.audit_duplicate_53

Write-Host ""
Write-Host "Repository-wide pytest is intentionally NOT run."
