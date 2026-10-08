$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=============================================================="
Write-Host "Phase 161-R4-R5 - pi_4^3 Proposition 5.1 Reference linkage"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/6] Validate current files with AST"
python -B -c "import ast, pathlib; files=['toda_prop56_zero_bootstrap.py','toda_group_proof_narrative_contribution_renderer.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/6] Apply Phase 161-R4-R5"
python -B `
  ".\phase161_r4_r5_pi4_3_prop51_reference_linkage\apply_phase161_r4_r5.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/6] Validate changed code without .pyc"
python -B -c "import ast, pathlib; files=['toda_prop56_zero_bootstrap.py','tests/test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation after apply: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Run R4-R5 focused tests"
python -B -m pytest -q `
  ".\tests\test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py" `
  ".\tests\test_phase161_r4_r4_restore_global_frontier.py" `
  ".\tests\test_phase161_r4_r3_fixed_frontier_internal_ancestry.py" `
  ".\tests\test_phase161_r4_repair1_pi4_2_semantic_frontier.py" `
  ".\tests\test_phase161_r4_pi4_2_specialization_frontier.py" `
  ".\tests\test_phase161_pi4_2_restored_reference_relink.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Run directly affected provenance regressions"
python -B -m pytest -q `
  ".\tests\test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py" `
  ".\tests\test_phase160_k1_generic_transport_connection.py" `
  ".\tests\test_phase59_prop53_integration.py" `
  ".\tests\test_phase59_n3_ehp_chain.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Print pi_4^2 Narrative"
python -B `
  ".\phase161_r4_r5_pi4_3_prop51_reference_linkage\verify_phase161_r4_r5.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R4-R5 completed."
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
