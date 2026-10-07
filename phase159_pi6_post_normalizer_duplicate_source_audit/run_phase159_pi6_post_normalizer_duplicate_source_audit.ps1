$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_6^3 post-normalizer duplicate source audit"
Write-Host "Audit only - isolate the Phase 159 post-normalizer stage"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/1] Trace the three Phase 159 post-normalizer transforms"
python "$PackageDir\audit_phase159_pi6_post_normalizer_duplicate_source.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit completed. No production files were modified."
Write-Host "=============================================================="
