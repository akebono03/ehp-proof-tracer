$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2"
Write-Host "Restore generic frontier prerequisite protection"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/5] Apply repair2"
python "$PackageRoot\apply_phase159_pi4_3_repair2.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair2 apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/5] Compile changed/new files"
python -m py_compile `
  ".\toda_group_proof_narrative_argument_multi_renderer.py" `
  ".\tests\test_phase159_pi4_3_repair2_frontier_prerequisite_protection.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/5] Run repair2 focused tests"
python -m pytest `
  tests/test_phase159_pi4_3_repair2_frontier_prerequisite_protection.py `
  tests/test_phase144_6_r4_supporting_fact_filtering.py `
  tests/test_phase143_36_argument_body_blocks.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair2 focused tests failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[4/5] Run Phase 159 direct-provenance regressions"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "Phase 159 provenance regression failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[5/5] Show public depth=2 Narrative"
python "$PackageRoot\audit_phase159_pi4_3_repair2_public_narrative.py"
if ($LASTEXITCODE -ne 0) {
  throw "public Narrative audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 repair2 complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
