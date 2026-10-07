$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_6^3 exactness injectivity duplicate audit"
Write-Host "Audit only - no production files are modified"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/2] Run duplicate pipeline audit"
python "$PackageDir\audit_phase159_pi6_exactness_injectivity_duplicate.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[2/2] Re-run final public dedup test for evidence"
python -m pytest -q `
  ".\tests\test_phase159_exactness_map_property_public_dedup.py::test_phase159_pi6_3_public_exactness_injectivity_is_emitted_once"
if ($LASTEXITCODE -eq 0) {
  Write-Host "Unexpectedly passed."
} else {
  Write-Host "Expected current failure reproduced."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit completed. No production files were modified."
Write-Host "=============================================================="
