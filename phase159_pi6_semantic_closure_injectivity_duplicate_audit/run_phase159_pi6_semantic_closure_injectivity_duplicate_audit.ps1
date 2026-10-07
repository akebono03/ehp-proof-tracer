$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_6^3 semantic-closure injectivity duplicate audit"
Write-Host "Audit only - no production files are modified"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/1] Compare base vs semantic-closure presentation"
python "$PackageDir\audit_phase159_pi6_semantic_closure_injectivity_duplicate.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit completed. No production files were modified."
Write-Host "=============================================================="
