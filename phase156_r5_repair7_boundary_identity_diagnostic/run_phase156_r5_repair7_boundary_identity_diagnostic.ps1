$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 repair7 - Reference boundary identity diagnostic"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python -m `
  phase156_r5_repair7_boundary_identity_diagnostic.diagnose_phase156_r5_repair7_boundary_identity
