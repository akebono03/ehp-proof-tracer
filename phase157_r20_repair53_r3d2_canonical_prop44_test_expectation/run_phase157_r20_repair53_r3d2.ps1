$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3d2 - canonical Prop.4.4 test expectation"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Test-only repair; corrected apply-script escaping"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host ""

Write-Host "[1/5] Apply test-only repair"
python ".\phase157_r20_repair53_r3d2_canonical_prop44_test_expectation\apply_phase157_r20_repair53_r3d2.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3d2 apply failed."
}

Write-Host ""
Write-Host "[2/5] Compile changed test"
python -m py_compile `
  ".\tests\test_phase157_r20_repair53_r3_fixed_reference_attribution.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3d2 compile check failed."
}

Write-Host ""
Write-Host "[3/5] Show and audit updated test function"
python ".\phase157_r20_repair53_r3d2_canonical_prop44_test_expectation\audit_phase157_r20_repair53_r3d2.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3d2 audit failed."
}

Write-Host ""
Write-Host "[4/5] Run repair53-r3 fixed-attribution tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3 fixed-attribution tests failed."
}

Write-Host ""
Write-Host "[5/5] Run repair53-r3c marker-remapping tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3c marker-remapping tests failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3d2 verification completed"
Write-Host "Production code changes: none"
Write-Host "Repository-wide pytest: NOT RUN (reserved for Phase 157 end)"
Write-Host "=============================================================="
