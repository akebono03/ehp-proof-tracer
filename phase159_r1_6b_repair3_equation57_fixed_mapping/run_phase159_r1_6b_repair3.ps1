$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-6b repair3 - Equation 5.7 fixed mapping"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Test changes: none"
Write-Host ""

Write-Host "[1/7] Apply repair3"
python ".\phase159_r1_6b_repair3_equation57_fixed_mapping\apply_phase159_r1_6b_repair3.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6b repair3 apply failed"
}

Write-Host ""
Write-Host "[2/7] Compile boundary file"
python -m py_compile `
  ".\toda_literature_statement_boundary.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed"
}

Write-Host ""
Write-Host "[3/7] Re-run Phase 157 R5-R3 catalog test"
python -m pytest -q `
  ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py"
if ($LASTEXITCODE -ne 0) {
  throw "Phase 157 R5-R3 catalog test failed"
}

Write-Host ""
Write-Host "[4/7] Run R1-6 focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6 focused tests failed"
}

Write-Host ""
Write-Host "[5/7] Re-run Phase 159 focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
if ($LASTEXITCODE -ne 0) {
  throw "Phase 159 focused tests failed"
}

Write-Host ""
Write-Host "[6/7] Run remaining related regressions"
python -m pytest -q `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase49_low_dimensional_facts.py" `
  ".\tests\test_phase49_generator_transport.py"
if ($LASTEXITCODE -ne 0) {
  throw "related regression failed"
}

Write-Host ""
Write-Host "[7/7] git diff --check and print pi_3^2 public narrative"
git diff --check
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed"
}

python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=2,k=1); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"
if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 preview failed"
}

Write-Host ""
Write-Host "PASS: Phase 159-R1-6b repair3 verification completed."
Write-Host "Full pytest was NOT run."
