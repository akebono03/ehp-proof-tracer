$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 repair5a test-only return-order fix"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply test-only repair5a"
python "$ScriptDir\apply_phase159_pi4_3_repair5a_test_fix.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Compile corrected test"
python -m py_compile `
  "tests/test_phase159_pi4_3_contribution_connector_ownership.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run Phase 159 pi4_3 focused tests"
python -m pytest `
  "tests/test_phase159_pi4_3_contribution_connector_ownership.py" `
  "tests/test_phase159_pi4_3_provenance_priority.py" `
  "tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Run directly related regressions"
python -m pytest `
  "tests/test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py" `
  "tests/test_phase144_6_r5_43_11c_r2_argument_participation_guard.py" `
  "tests/test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py" `
  "tests/test_phase157_r20_repair43_dangling_connector_cleanup.py" `
  "tests/test_phase50_pi4_3_finite_cyclic.py" `
  "tests/test_phase50_pi4_3_exactness_bridge.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Repair5a focused verification complete."
Write-Host "Full test suite was not run."
