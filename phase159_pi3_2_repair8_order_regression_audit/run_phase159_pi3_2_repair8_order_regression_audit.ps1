$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 repair8 order regression audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/3] Compile audit script"
python -m py_compile `
  "$ScriptDir\audit_phase159_pi3_2_repair8_order_regression.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/3] Run existing Phase 159 pi3_2 focused contract"
python -m pytest `
  "tests/test_phase159_r1_2_pi3_2_narrative_repair.py" `
  -q
$Pi32TestExit = $LASTEXITCODE

Write-Host ""
Write-Host "[3/3] Run placement/stage audit"
python "$ScriptDir\audit_phase159_pi3_2_repair8_order_regression.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Existing pi3_2 test exit code: $Pi32TestExit"
Write-Host "Audit output:"
Write-Host "$ScriptDir\phase159_pi3_2_repair8_order_regression_audit.txt"

if ($Pi32TestExit -ne 0) {
  Write-Host ""
  Write-Host "The existing Phase 159 pi3_2 contract currently fails."
}

exit 0
