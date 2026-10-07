$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-6b - Toda (5.1) attribution + map-property numbering"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/7] Apply R1-6b"
python ".\phase159_r1_6b_toda51_attribution_map_property_numbering\apply_phase159_r1_6b.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6b apply failed"
}

Write-Host ""
Write-Host "[2/7] Compile changed files"
python -m py_compile `
  ".\toda_literature_statement_boundary.py" `
  ".\toda_upstream_bootstrap.py" `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed"
}

Write-Host ""
Write-Host "[3/7] Run R1-6 focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6 focused tests failed"
}

Write-Host ""
Write-Host "[4/7] Re-run Phase 159 focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
if ($LASTEXITCODE -ne 0) {
  throw "Phase 159 focused tests failed"
}

Write-Host ""
Write-Host "[5/7] Run related literature-boundary/reference regressions"
python -m pytest -q `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py" `
  ".\tests\test_phase49_low_dimensional_facts.py" `
  ".\tests\test_phase49_generator_transport.py"
if ($LASTEXITCODE -ne 0) {
  throw "related regression failed"
}

Write-Host ""
Write-Host "[6/7] git diff --check"
git diff --check
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed"
}

Write-Host ""
Write-Host "[7/7] Print pi_3^2 public narrative"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=2,k=1); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"
if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 preview failed"
}

Write-Host ""
Write-Host "PASS: Phase 159-R1-6b focused verification completed."
Write-Host "Full pytest was NOT run."
