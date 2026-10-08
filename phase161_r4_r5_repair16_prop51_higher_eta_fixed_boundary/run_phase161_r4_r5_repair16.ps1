$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=============================================================="
Write-Host "Phase 161-R4-R5 repair16 - Prop.5.1 higher-eta fixed boundary"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/6] Validate current files and package test"
python -B -c "import ast, pathlib; files=['toda_literature_statement_boundary.py','toda_group_proof_narrative_references.py','toda_group_proof_narrative_contribution_renderer.py','phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary/test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.template.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/6] Apply repair16"
python -B `
  ".\phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary\apply_phase161_r4_r5_repair16.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/6] Validate changed code"
python -B -c "import ast, pathlib; files=['toda_literature_statement_boundary.py','tests/test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8'), filename=f) for f in files]; print('AST validation after apply: PASS')"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/6] Run focused Phase161 R4-R5 tests"
python -B -m pytest -q `
  ".\tests\test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.py" `
  ".\tests\test_phase161_r4_r5_repair14_reference_locator_dedup.py" `
  ".\tests\test_phase161_r4_r5_repair13_reference_selection_source_binding.py" `
  ".\tests\test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py" `
  ".\tests\test_phase161_r4_r5_repair9a_final_public_reference_relink.py" `
  ".\tests\test_phase161_r4_r5_repair6_backward_self_marker_relink.py" `
  ".\tests\test_phase161_r4_r5_repair3_reference_self_marker_relink.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/6] Run current boundary and Phase157 reference contracts"
python -B -m pytest -q `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase157_r20_repair12_map_property_reference_support.py" `
  ".\tests\test_phase157_r19_pi6_3_reference_dependency_restoration.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[6/6] Print final pi_4^2 Narrative"
python -B `
  ".\phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary\verify_phase161_r4_r5_repair16.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 161-R4-R5 repair16 completed."
Write-Host "Full test suite: NOT RUN"
Write-Host "=============================================================="
