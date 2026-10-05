$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r5 - pi15 fixed-component Reference linkage"
Write-Host "=============================================================="
Write-Host "Production change:"
Write-Host "  toda_group_proof_narrative_renderer.py"
Write-Host "Focused pytest only"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host ""

Write-Host "[1/5] Apply repair53-r5"
python ".\phase157_r20_repair53_r5_pi15_fixed_component_reference_linkage\apply_phase157_r20_repair53_r5.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r5 apply failed."
}

Write-Host ""
Write-Host "[2/5] Compile changed production and focused test"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r5 compile check failed."
}

Write-Host ""
Write-Host "[3/5] Run updated pi15 fixed-component tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r5 focused tests failed."
}

Write-Host ""
Write-Host "[4/5] Re-run repair53-r3 fixed-attribution tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3 fixed-attribution regression failed."
}

Write-Host ""
Write-Host "[5/5] Public pi15^8 audit"
python ".\phase157_r20_repair53_r5_pi15_fixed_component_reference_linkage\audit_phase157_r20_repair53_r5.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r5 public audit failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r5 verification completed"
Write-Host "Repository-wide pytest: NOT RUN (reserved for Phase 157 end)"
Write-Host "=============================================================="
