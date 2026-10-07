$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - repair2g fix10b"
Write-Host "Generic numbered map-property display normalization"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/5] Apply fix10b"
python "$PackageRoot\apply_phase159_pi4_3_repair2g_fix10b.py"
if ($LASTEXITCODE -ne 0) {
  throw "fix10b apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/5] Audit pi_3^2 wording and pi_4^3 Reference"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix10b.py"
if ($LASTEXITCODE -ne 0) {
  throw "fix10b public Narrative audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/5] Run pi_3^2 Narrative contract"
python -m pytest `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 Narrative contract failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[4/5] Run repair2g focused tests"
python -m pytest `
  tests/test_phase159_pi4_3_repair2g_reference_policy.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair2g focused tests failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[5/5] Run repair1 health checks"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair1 health checks failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "fix10b complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
