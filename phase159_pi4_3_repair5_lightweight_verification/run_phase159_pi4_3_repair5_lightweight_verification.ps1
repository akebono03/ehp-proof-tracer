$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi4_3 repair5 lightweight verification"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Compile verification script"
python -m py_compile `
  "$ScriptDir\verify_phase159_pi4_3_repair5_public_output.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Run Phase 157 dangling-connector regression"
python -m pytest `
  "tests/test_phase157_r20_repair43_dangling_connector_cleanup.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run Phase 50 pi4_3 inference regressions"
python -m pytest `
  "tests/test_phase50_pi4_3_finite_cyclic.py" `
  "tests/test_phase50_pi4_3_exactness_bridge.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Show and verify current pi4_3 public Narrative"
python "$ScriptDir\verify_phase159_pi4_3_repair5_public_output.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Lightweight verification complete."
Write-Host "Heavy Phase 144 cross-group fixtures were intentionally not rerun."
Write-Host "Full test suite was not run."
