$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 exactness-reason stale expectation repair6a"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply test-only repair6a"
python "$ScriptDir\apply_phase159_exactness_reason_stale_expectation_repair6a.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Compile changed test"
python -m py_compile `
  "tests/test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run exactness-reason focused tests"
python -m pytest `
  "tests/test_phase150_rc4_5c_2_exactness_to_map_property.py" `
  "tests/test_phase157_r20_repair43_dangling_connector_cleanup.py" `
  "tests/test_phase157_r11_r17_residual_narrative_defects.py::test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Re-run Phase 159 pi4_3 focused tests"
python -m pytest `
  "tests/test_phase159_pi4_3_contribution_connector_ownership.py" `
  "tests/test_phase159_pi4_3_provenance_priority.py" `
  "tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Repair6a focused verification complete."
Write-Host "Heavy Phase 144 cross-group fixtures were not run."
Write-Host "Full test suite was not run."
