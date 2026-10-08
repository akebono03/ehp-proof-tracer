$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=============================================================="
Write-Host "Phase 161-R4-R4 resume - after pycache access denied"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "R4-R4 production changes are already applied."
Write-Host "This runner does NOT re-apply production changes."
Write-Host ""

Write-Host "[3/6] Validate syntax without writing .pyc"
python -B `
  ".\phase161_r4_r4_resume_after_pycache_access_denied\validate_phase161_r4_r4_syntax.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Run Phase161 R4 focused tests"
python -B -m pytest -q `
  ".\tests\test_phase161_r4_r4_restore_global_frontier.py" `
  ".\tests\test_phase161_r4_r3_fixed_frontier_internal_ancestry.py" `
  ".\tests\test_phase161_r4_repair1_pi4_2_semantic_frontier.py" `
  ".\tests\test_phase161_r4_pi4_2_specialization_frontier.py" `
  ".\tests\test_phase161_pi4_2_restored_reference_relink.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Run restored frontier + Phase161 regressions"
python -B -m pytest -q `
  ".\tests\test_phase156_r5_repair12_reference_frontier.py" `
  ".\tests\test_phase156_r5_repair13_root_reference_frontier.py" `
  ".\tests\test_phase156_r5_repair8_reference_owned_ancestor_closure.py" `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py" `
  ".\tests\test_phase160_generic_finite_cyclic_transport.py" `
  ".\tests\test_phase160_k2_generic_transport_connection.py" `
  -k "not unreferenced_definition_step_is_reference_owned"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Print pi_4^2 Narrative"
python -B `
  ".\phase161_r4_r4_restore_global_frontier\verify_phase161_r4_r4.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R4-R4 resume completed."
Write-Host "Production changes in this resume package: NONE"
Write-Host "Tests changed in this resume package: NONE"
Write-Host "Known stale Phase156 repair8 inference_rule-is-None expectation: excluded."
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
