$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 semantic final-conclusion dedup"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/3] Apply implementation"
python "$ScriptDir\apply_phase159_pi4_3_semantic_final_conclusion_dedup.py"

Write-Host ""
Write-Host "[2/3] Run focused semantic-dedup tests"
python -m pytest `
  "tests/test_phase159_pi4_3_semantic_final_conclusion_dedup.py" `
  -q

Write-Host ""
Write-Host "[3/3] Run directly related existing tests"
python -m pytest `
  "tests/test_phase50_pi4_3_finite_cyclic.py" `
  "tests/test_phase50_pi4_3_exactness_bridge.py" `
  "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
  -q

Write-Host ""
Write-Host "Focused verification complete."
Write-Host "Full test suite was not run."
