$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3d3 - canonical Prop.4.4 audit fix"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Test changes: none"
Write-Host "Audit-script-only repair"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host ""

Write-Host "[1/4] Compile existing modified test"
python -m py_compile `
  ".\tests\test_phase157_r20_repair53_r3_fixed_reference_attribution.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3d3 compile check failed."
}

Write-Host ""
Write-Host "[2/4] Audit canonical Prop.4.4 source expectation"
python ".\phase157_r20_repair53_r3d3_canonical_prop44_audit_fix\audit_phase157_r20_repair53_r3d3.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3d3 audit failed."
}

Write-Host ""
Write-Host "[3/4] Run repair53-r3 fixed-attribution tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3 fixed-attribution tests failed."
}

Write-Host ""
Write-Host "[4/4] Run repair53-r3c marker-remapping tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3c marker-remapping tests failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3d3 verification completed"
Write-Host "Production code changes: none"
Write-Host "Test changes in this package: none"
Write-Host "Repository-wide pytest: NOT RUN (reserved for Phase 157 end)"
Write-Host "=============================================================="
