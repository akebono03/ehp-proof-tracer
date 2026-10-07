$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

function Invoke-PythonStep {
  param(
    [string]$Description,
    [string[]]$Arguments
  )

  Write-Host $Description
  & python @Arguments

  if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "FAILED: $Description"
    exit $LASTEXITCODE
  }
}

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 exactness reason locality repair7"
Write-Host "Re-apply exactness locality after map-property ordering"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Invoke-PythonStep `
  "[1/4] Apply repair7" `
  @(
    (Join-Path $PackageDir "apply_phase159_pi3_2_exactness_reason_locality_repair7.py")
  )

Write-Host ""
Invoke-PythonStep `
  "[2/4] Exactness locality repair7 audit" `
  @(
    (Join-Path $PackageDir "audit_phase159_pi3_2_exactness_reason_locality_repair7.py")
  )

Write-Host ""
Write-Host "[3/4] Focused Phase 159 tests"
& python -m pytest `
  ".\tests\test_phase159_pi3_2_exactness_reason_locality.py" `
  ".\tests\test_phase159_pi3_2_map_property_order.py" `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "FAILED: focused pytest"
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Public pi_3^2 narrative"
& python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=2,k=1); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "FAILED: public narrative render"
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Repair7 focused verification finished."
Write-Host "Full suite is intentionally NOT run in this Phase 159 substep."
