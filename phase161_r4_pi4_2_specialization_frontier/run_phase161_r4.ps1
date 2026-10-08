$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R4 - pi_4^2 specialization + Reference frontier"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/6] Validate current recovered/R3 renderer"
python -m py_compile `
  ".\toda_group_proof_narrative_contribution_renderer.py" `
  ".\toda_group_proof_narrative_references.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/6] Apply Phase 161-R4 minimal repair"
python `
  ".\phase161_r4_pi4_2_specialization_frontier\apply_phase161_r4.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/6] Compile changed production files"
python -m py_compile `
  ".\toda_group_proof_narrative_contribution_renderer.py" `
  ".\toda_group_proof_narrative_references.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Run Phase 161-R4 focused tests"
python -m pytest -q `
  ".\tests\test_phase161_r4_pi4_2_specialization_frontier.py" `
  ".\tests\test_phase161_pi4_2_restored_reference_relink.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Run Phase 161 baseline focused regressions"
python -m pytest -q `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py" `
  ".\tests\test_phase160_generic_finite_cyclic_transport.py" `
  ".\tests\test_phase160_k2_generic_transport_connection.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Print Phase 161-R4 pi_4^2 Narrative"
python `
  ".\phase161_r4_pi4_2_specialization_frontier\verify_phase161_r4.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R4 completed."
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
