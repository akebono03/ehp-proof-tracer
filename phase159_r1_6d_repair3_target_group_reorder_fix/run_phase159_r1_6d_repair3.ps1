$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-6d repair3 - target-group reorder fix"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/7] Apply repair3"
python ".\phase159_r1_6d_repair3_target_group_reorder_fix\apply_phase159_r1_6d_repair3.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6d repair3 apply failed"
}

Write-Host ""
Write-Host "[2/7] Compile renderer"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed"
}

Write-Host ""
Write-Host "[3/7] Run repair2 ordering focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_6d_target_group_fact_order.py"
if ($LASTEXITCODE -ne 0) {
  throw "ordering focused tests failed"
}

Write-Host ""
Write-Host "[4/7] Re-run R1-6d tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_6d_specialization_reference_linkage_finalization.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6d tests failed"
}

Write-Host ""
Write-Host "[5/7] Re-run R1-6a/R1-6b/R1-6c + Phase159 focused"
python -m pytest -q `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py" `
  ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
if ($LASTEXITCODE -ne 0) {
  throw "Phase159 focused regressions failed"
}

Write-Host ""
Write-Host "[6/7] Run related boundary/reference regressions"
python -m pytest -q `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py" `
  ".\tests\test_phase49_low_dimensional_facts.py" `
  ".\tests\test_phase49_generator_transport.py"
if ($LASTEXITCODE -ne 0) {
  throw "related regressions failed"
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
Write-Host "PASS: Phase 159-R1-6d repair3 verification completed."
Write-Host "Full pytest was NOT run."
