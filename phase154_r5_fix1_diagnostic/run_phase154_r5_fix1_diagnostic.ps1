$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R5 Fix1 Diagnostic"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host ""

python ".\phase154_r5_fix1_diagnostic\diagnose_phase154_r5_fix1.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 Fix1 diagnostic failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R5 Fix1 diagnostic completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN"
