$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 semantic final-conclusion dedup repair1"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply repair1"
python "$ScriptDir\apply_phase159_pi4_3_semantic_final_conclusion_dedup_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Compile changed modules"
python -m py_compile `
  "toda_group_proof_narrative_statement_identity.py" `
  "toda_group_proof_narrative_contribution_renderer.py" `
  "tests/test_phase159_pi4_3_semantic_final_conclusion_dedup.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run focused Phase 159 tests"
python -m pytest `
  "tests/test_phase159_pi4_3_semantic_final_conclusion_dedup.py" `
  "tests/test_phase159_r1_2_pi3_2_narrative_repair.py" `
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
Write-Host "Repair1 focused verification complete."
Write-Host "Full test suite was not run."
