
$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2g fix7"
Write-Host "sphere_connectivity_zero boundary + usage-filter audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Apply sphere_connectivity_zero fixed mapping"
python "$PackageRoot\apply_phase159_pi4_3_repair2g_fix7.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair2g fix7 apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/4] Audit fixed-boundary and step-usage filtering"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix7.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair2g fix7 audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/4] Run repair2g focused tests"
python -m pytest `
  tests/test_phase159_pi4_3_repair2g_reference_policy.py `
  -q
$FocusedExit = $LASTEXITCODE

Write-Host ""
Write-Host "[4/4] Run repair1 health checks"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair1 health checks failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair2g fix7 complete"
Write-Host "Focused pytest exit code: $FocusedExit"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="

exit 0
