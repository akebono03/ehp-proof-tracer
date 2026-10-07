$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159-R1-3 repair3 - generic definition node traversal"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/6] Apply repair3"
python ".\phase159_r1_3_repair3_definition_node_walk\apply_phase159_r1_3_repair3.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair3 apply failed"
}

Write-Host ""
Write-Host "[2/6] Compile renderer"
python -m py_compile ".\toda_group_proof_narrative_renderer.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed"
}

Write-Host ""
Write-Host "[3/6] Run Phase 159 focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
if ($LASTEXITCODE -ne 0) {
  throw "Phase 159 focused tests failed"
}

Write-Host ""
Write-Host "[4/6] Run definition/inference regressions"
python -m pytest -q `
  ".\tests\test_phase49_generator_transport.py" `
  ".\tests\test_phase143_71a_eta_definition_visibility.py"
if ($LASTEXITCODE -ne 0) {
  throw "definition/inference regression failed"
}

Write-Host ""
Write-Host "[5/6] git diff --check"
git diff --check
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed"
}

Write-Host ""
Write-Host "[6/6] Print pi_3^2 public narrative"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=2,k=1); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"
if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 preview failed"
}

Write-Host ""
Write-Host "PASS: Phase 159-R1-3 repair3 focused verification completed."
Write-Host "Full pytest was NOT run."
