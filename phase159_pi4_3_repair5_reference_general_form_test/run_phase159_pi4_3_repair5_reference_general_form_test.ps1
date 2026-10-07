$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi4^3 repair5"
Write-Host "(5.1) general-form stale test repair"
Write-Host "=============================================================="

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Set-Location $RepositoryRoot

Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Write-Host "[1/4] Apply stale test repair"
python "$PackageRoot\apply_phase159_pi4_3_repair5_reference_general_form_test.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Focused pi4^3 reference-policy test"
python -m pytest `
  ".\tests\test_phase159_pi4_3_repair2g_reference_policy.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Stable-transport and related pi4^3 regression tests"
python -m pytest `
  ".\tests\test_phase159_pi_nplus1_n_stable_transport.py" `
  ".\tests\test_phase153_r2_toda45_map_property_semantic.py" `
  ".\tests\test_phase159_pi4_3_trailing_premise_order.py" `
  ".\tests\test_phase159_pi4_3_exactness_surjectivity_unification.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Show pi_5^4 Narrative"
python -c "from tests.test_phase143_19_method_evidence import _method_evidence_data; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; p,_,_,_=_method_evidence_data(4,1); print(render_toda_group_proof_narrative_markdown(p))"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair5 focused verification completed"
Write-Host "Production code was NOT changed."
Write-Host "Full test suite was NOT run."
Write-Host "=============================================================="
