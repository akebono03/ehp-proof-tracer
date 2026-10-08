$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 161-R4-R3 - fixed frontier internal ancestry"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/6] Validate current R4 state"
python -m py_compile `
  ".\toda_group_proof_narrative_contribution_renderer.py" `
  ".\toda_group_proof_narrative_references.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/6] Apply Phase 161-R4-R3 minimal repair"
python `
  ".\phase161_r4_r3_fixed_frontier_internal_ancestry\apply_phase161_r4_r3.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/6] Compile changed production file"
python -m py_compile `
  ".\toda_group_proof_narrative_contribution_renderer.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Run Phase 161-R4 focused tests"
python -m pytest -q `
  ".\tests\test_phase161_r4_r3_fixed_frontier_internal_ancestry.py" `
  ".\tests\test_phase161_r4_repair1_pi4_2_semantic_frontier.py" `
  ".\tests\test_phase161_r4_pi4_2_specialization_frontier.py" `
  ".\tests\test_phase161_pi4_2_restored_reference_relink.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Run frontier + Phase161 focused regressions"
python -m pytest -q `
  ".\tests\test_phase156_r5_repair8_reference_owned_ancestor_closure.py" `
  ".\tests\test_phase156_r5_repair12_reference_frontier.py" `
  ".\tests\test_phase156_r5_repair13_root_reference_frontier.py" `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py" `
  ".\tests\test_phase160_generic_finite_cyclic_transport.py" `
  ".\tests\test_phase160_k2_generic_transport_connection.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Print repaired pi_4^2 public Narrative"
python `
  ".\phase161_r4_r3_fixed_frontier_internal_ancestry\verify_phase161_r4_r3.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R4-R3 completed."
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
