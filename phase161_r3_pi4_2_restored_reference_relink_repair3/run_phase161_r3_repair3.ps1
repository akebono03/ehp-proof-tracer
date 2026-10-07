$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R3 repair3 - pi_4^2 restored Reference relink"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/5] Validate recovered renderer"
python -m py_compile `
  ".\toda_group_proof_narrative_contribution_renderer.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/5] Apply Phase 161-R3 minimal repair"
python `
  ".\phase161_r3_pi4_2_restored_reference_relink_repair3\apply_phase161_r3_repair3.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/5] Run Phase 161-R3 focused test"
python -m pytest -q `
  ".\tests\test_phase161_pi4_2_restored_reference_relink.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/5] Run Phase 161 baseline focused regressions"
python -m pytest -q `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py" `
  ".\tests\test_phase160_generic_finite_cyclic_transport.py" `
  ".\tests\test_phase160_k2_generic_transport_connection.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/5] Print repaired pi_4^2 public Narrative"
python `
  ".\phase161_r3_pi4_2_restored_reference_relink_repair3\verify_phase161_r3_repair3.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R3 repair3 completed."
Write-Host "Known unrelated Phase157 repair12 failures: not used as R3 gate."
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
