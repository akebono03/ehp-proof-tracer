$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 visible dependency topological ordering repair1"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/4] Apply repair1"
python (Join-Path $PackageDir "apply_phase159_pi3_2_visible_dependency_topological_order_repair1.py")

Write-Host ""
Write-Host "[2/4] Dependency-edge audit"
python (Join-Path $PackageDir "audit_phase159_pi3_2_visible_dependency_edges.py")

Write-Host ""
Write-Host "[3/4] Focused Phase 159 tests"
python -m pytest `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q

Write-Host ""
Write-Host "[4/4] Public pi_3^2 narrative"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=2,k=1); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"

Write-Host ""
Write-Host "Repair1 focused verification finished."
Write-Host "Full suite is intentionally NOT run in this Phase 159 substep."
