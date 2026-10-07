$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 final-connector repair4"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply repair4"
python "$ScriptDir\apply_phase159_pi4_3_final_connector_repair4.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Compile changed files"
python -m py_compile `
  "toda_group_proof_narrative_contribution_renderer.py" `
  "tests/test_phase159_pi4_3_final_connector_repair.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run focused connector and duplicate tests"
python -m pytest `
  "tests/test_phase159_pi4_3_final_connector_repair.py" `
  "tests/test_phase159_pi4_3_provenance_priority.py" `
  "tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py" `
  "tests/test_phase157_r20_repair43_dangling_connector_cleanup.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Run directly related group-structure regression tests"
python -m pytest `
  "tests/test_phase143_59b_group_structure_duplicate_suppression.py" `
  "tests/test_phase50_pi4_3_finite_cyclic.py" `
  "tests/test_phase50_pi4_3_exactness_bridge.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Repair4 focused verification complete."
Write-Host "Full test suite was not run."
