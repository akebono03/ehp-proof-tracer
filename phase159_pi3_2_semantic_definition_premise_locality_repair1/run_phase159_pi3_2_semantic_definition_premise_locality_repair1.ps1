$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 semantic definition-premise locality repair1"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/4] Apply repair"
python "$PackageDir\apply_phase159_pi3_2_semantic_definition_premise_locality_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Run focused locality/order tests"
python -m pytest `
  tests/test_phase159_pi3_2_map_property_order.py `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run related pi3_2 narrative contract tests"
python -m pytest `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py `
  tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Print current pi3_2 public Narrative"
python "$PackageDir\show_phase159_pi3_2_public_narrative.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Focused verification complete."
Write-Host "Full pytest is intentionally not run here; run it only at the end of the Phase."
