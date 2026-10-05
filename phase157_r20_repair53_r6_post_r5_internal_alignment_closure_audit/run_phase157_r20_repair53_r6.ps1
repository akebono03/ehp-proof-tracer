$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r6 - post-r5 internal alignment closure audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Test changes: none"
Write-Host "Focused regression + audit only"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host ""

Write-Host "[1/4] Compile audit and current r5 production file"
python -m py_compile `
  ".\phase157_r20_repair53_r6_post_r5_internal_alignment_closure_audit\audit_phase157_r20_repair53_r6.py" `
  ".\toda_group_proof_narrative_renderer.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r6 compile check failed."
}

Write-Host ""
Write-Host "[2/4] Run repair53-r5 / r3c focused tests"
python -m pytest `
  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r5/r3c focused regression failed."
}

Write-Host ""
Write-Host "[3/4] Run repair53-r3 fixed-attribution regression"
python -m pytest `
  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r3 fixed-attribution regression failed."
}

Write-Host ""
Write-Host "[4/4] Run post-r5 internal alignment closure audit"
python ".\phase157_r20_repair53_r6_post_r5_internal_alignment_closure_audit\audit_phase157_r20_repair53_r6.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r6 closure audit failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r6 closure verification completed"
Write-Host "Production code changes: none"
Write-Host "Test changes: none"
Write-Host "Repository-wide pytest: NOT RUN (reserved for Phase 157 end)"
Write-Host "=============================================================="
