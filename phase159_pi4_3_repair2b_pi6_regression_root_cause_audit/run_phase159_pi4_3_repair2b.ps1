$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2b"
Write-Host "pi_6^3 regression root-cause audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Run pi_6^3 regression decomposition audit"
python "$PackageRoot\audit_phase159_pi4_3_repair2b_pi6_regression_root_cause.py"
if ($LASTEXITCODE -ne 0) {
  throw "pi_6^3 regression audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/2] Run only Phase 159 repair1 health checks"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair1 health checks failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
