$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 provenance-priority repair3"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply repair3"
python "$ScriptDir\apply_phase159_pi4_3_provenance_priority_repair3.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Compile changed files"
python -m py_compile `
  "toda_group_proof_narrative_argument_body_renderer.py" `
  "tests/test_phase159_pi4_3_provenance_priority.py" `
  "tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run focused duplicate/provenance tests"
python -m pytest `
  "tests/test_phase159_pi4_3_provenance_priority.py" `
  "tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py" `
  "tests/test_phase143_59b_group_structure_duplicate_suppression.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Run pi4_3 inference regression tests"
python -m pytest `
  "tests/test_phase50_pi4_3_finite_cyclic.py" `
  "tests/test_phase50_pi4_3_exactness_bridge.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Repair3 focused verification complete."
Write-Host "Full test suite was not run."
