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
Write-Host "Phase 159 pi3_2 public definition-premise locality repair18"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Invoke-PythonStep `
  "[1/4] Apply repair18" `
  @(
    (Join-Path $PackageDir "apply_phase159_pi3_2_public_definition_premise_locality_repair18.py")
  )

Write-Host ""
Invoke-PythonStep `
  "[2/4] Public definition-premise locality audit" `
  @(
    (Join-Path $PackageDir "audit_phase159_pi3_2_public_definition_premise_locality_repair18.py")
  )

Write-Host ""
Write-Host "[3/4] Focused Phase 159 tests"
& python -m pytest `
  ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py" `
  ".\tests\test_phase159_pi3_2_post_reference_locality_reapply.py" `
  ".\tests\test_phase159_pi3_2_final_locality_reapply.py" `
  ".\tests\test_phase159_pi3_2_proofstep_premise_locality.py" `
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
& python -c "from tests.test_phase143_19_method_evidence import _method_evidence_data; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; p,_,_,_=_method_evidence_data(2,1); print(render_toda_group_proof_narrative_markdown(p))"

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "FAILED: public narrative render"
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Repair18 focused verification finished."
Write-Host "Full suite is intentionally NOT run in this Phase 159 substep."
