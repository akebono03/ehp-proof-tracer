$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 semantic definition-premise locality rule"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/3] Apply implementation and focused test"
python "$PackageDir\apply_phase159_pi3_2_semantic_definition_premise_locality.py"

Write-Host ""
Write-Host "[2/3] Run focused locality/order test"
python -m pytest `
  tests/test_phase159_pi3_2_map_property_order.py `
  -q

Write-Host ""
Write-Host "[3/3] Run related pi3_2 narrative contract tests"
python -m pytest `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py `
  tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py `
  -q

Write-Host ""
Write-Host "Focused verification complete."
Write-Host "Full pytest is intentionally not run here; run it only at the end of the Phase."
