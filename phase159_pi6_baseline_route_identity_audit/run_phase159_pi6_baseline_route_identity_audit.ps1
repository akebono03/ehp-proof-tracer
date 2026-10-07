$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_6^3 baseline route identity audit"
Write-Host "Audit only - fresh presentation / closure idempotence"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/1] Compare manual baseline vs actual baseline vs direct public"
python "$PackageDir\audit_phase159_pi6_baseline_route_identity.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit completed. No production files were modified."
Write-Host "=============================================================="
