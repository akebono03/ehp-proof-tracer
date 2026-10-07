$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-3 repair5 - stale Phase 150 expectation"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host ""

Write-Host "[1/6] Apply test-only repair"
python ".\phase159_r1_3_repair5_stale_phase150_expectation\apply_phase159_r1_3_repair5.py"
if ($LASTEXITCODE -ne 0) { throw "repair5 apply failed" }

Write-Host "[2/6] Run repaired Phase 150 test file"
python -m pytest -q ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) { throw "Phase 150 focused test failed" }

Write-Host "[3/6] Re-run Phase 159 focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
if ($LASTEXITCODE -ne 0) { throw "Phase 159 focused tests failed" }

Write-Host "[4/6] Re-run related regressions"
python -m pytest -q `
  ".\tests\test_phase49_generator_transport.py" `
  ".\tests\test_phase143_71a_eta_definition_visibility.py" `
  ".\tests\test_phase143_32_exactness_component_latex.py" `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
if ($LASTEXITCODE -ne 0) { throw "related regression failed" }

Write-Host "[5/6] git diff --check"
git diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }

Write-Host "[6/6] Print pi_3^2 public narrative"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=2,k=1); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"
if ($LASTEXITCODE -ne 0) { throw "pi_3^2 preview failed" }

Write-Host "PASS: Phase 159-R1-3 repair5 focused verification completed."
Write-Host "Full pytest was NOT run."
