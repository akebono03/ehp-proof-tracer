$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=============================================================="
Write-Host "Phase 161-R4-R5 repair14 - Reference locator dedup"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/6] Validate current files and package templates"
python -B -c "import ast, pathlib; files=['toda_group_proof_narrative_references.py','toda_group_proof_narrative_contribution_renderer.py','phase161_r4_r5_repair14_reference_locator_dedup/build_toda_group_proof_narrative_reference_entries.template.py','phase161_r4_r5_repair14_reference_locator_dedup/test_phase161_r4_r5_repair14_reference_locator_dedup.template.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/6] Apply repair14"
python -B `
  ".\phase161_r4_r5_repair14_reference_locator_dedup\apply_phase161_r4_r5_repair14.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/6] Validate changed code"
python -B -c "import ast, pathlib; files=['toda_group_proof_narrative_references.py','tests/test_phase161_r4_r5_repair14_reference_locator_dedup.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation after apply: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Run focused Reference tests"
python -B -m pytest -q `
  ".\tests\test_phase161_r4_r5_repair14_reference_locator_dedup.py" `
  ".\tests\test_phase161_r4_r5_repair13_reference_selection_source_binding.py" `
  ".\tests\test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py" `
  ".\tests\test_phase144_6_r3_production_references.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Run directly affected R4 linkage regressions"
python -B -m pytest -q `
  ".\tests\test_phase161_r4_r5_repair9a_final_public_reference_relink.py" `
  ".\tests\test_phase161_r4_r5_repair6_backward_self_marker_relink.py" `
  ".\tests\test_phase161_r4_r5_repair3_reference_self_marker_relink.py" `
  ".\tests\test_phase161_r4_r4_restore_global_frontier.py" `
  ".\tests\test_phase161_r4_r3_fixed_frontier_internal_ancestry.py" `
  ".\tests\test_phase161_r4_repair1_pi4_2_semantic_frontier.py" `
  ".\tests\test_phase161_r4_pi4_2_specialization_frontier.py" `
  ".\tests\test_phase161_pi4_2_restored_reference_relink.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Print Reference entries and final pi_4^2 Narrative"
python -B `
  ".\phase161_r4_r5_repair14_reference_locator_dedup\verify_phase161_r4_r5_repair14.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R4-R5 repair14 completed."
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
