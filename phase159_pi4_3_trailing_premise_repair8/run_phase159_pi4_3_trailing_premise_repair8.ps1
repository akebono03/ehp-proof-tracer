$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 trailing-premise repair8"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/5] Apply repair8"
python "$ScriptDir\apply_phase159_pi4_3_trailing_premise_repair8.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/5] Compile changed production and focused test"
python -m py_compile `
  "toda_group_proof_narrative_contribution_renderer.py" `
  "tests/test_phase159_pi4_3_trailing_premise_order.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/5] Run new pi4_3 trailing-premise tests"
python -m pytest `
  "tests/test_phase159_pi4_3_trailing_premise_order.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/5] Re-run Phase 159 pi4_3 focused tests"
python -m pytest `
  "tests/test_phase159_pi4_3_contribution_connector_ownership.py" `
  "tests/test_phase159_pi4_3_provenance_priority.py" `
  "tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/5] Re-run pi6_3 exactness/order focused regressions"
python -m pytest `
  "tests/test_phase159_pi6_3_zero_map_reason_order.py" `
  "tests/test_phase150_rc4_5c_2_exactness_to_map_property.py" `
  "tests/test_phase157_r20_repair43_dangling_connector_cleanup.py" `
  "tests/test_phase157_r11_r17_residual_narrative_defects.py::test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Repair8 focused verification complete."
Write-Host "Heavy Phase 144 cross-group fixtures were not run."
Write-Host "Full test suite was not run."
