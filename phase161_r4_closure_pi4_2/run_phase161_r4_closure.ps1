$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=============================================================="
Write-Host "Phase 161-R4 closure - pi_4^2"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Validate current Phase161 R4 files with AST"
python -B -c "import ast, pathlib; files=['toda_group_proof_narrative_contribution_renderer.py','toda_group_proof_narrative_references.py','tests/test_phase161_r4_r4_restore_global_frontier.py','tests/test_phase161_r4_r3_fixed_frontier_internal_ancestry.py','tests/test_phase161_r4_repair1_pi4_2_semantic_frontier.py','tests/test_phase161_r4_pi4_2_specialization_frontier.py','tests/test_phase161_pi4_2_restored_reference_relink.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Run Phase161 R4 focused tests"
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
Write-Host "[3/4] Verify pi_4^2 public Narrative and completion criteria"
python -B `
  ".\phase161_r4_closure_pi4_2\verify_phase161_r4_closure.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Record known pre-existing Phase157 pi_6^3 Reference regression"
python -B `
  ".\phase161_r4_closure_pi4_2\show_known_phase157_regression.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R4 closure completed."
Write-Host "Production changes in closure: NONE"
Write-Host "Test changes in closure: NONE"
Write-Host "Full test suite: NOT RUN"
Write-Host "Next Phase161 step: audit pi_5^3"
Write-Host "=============================================================="
