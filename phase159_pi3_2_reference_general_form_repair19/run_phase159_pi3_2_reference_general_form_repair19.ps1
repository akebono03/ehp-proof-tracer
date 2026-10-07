$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 Reference general-form repair19"
Write-Host "Toda (5.1) fixed-statement restoration only"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/4] Apply Reference-only repair"
python ".\phase159_pi3_2_reference_general_form_repair19\apply_phase159_pi3_2_reference_general_form_repair19.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Syntax check"
python -m py_compile ".\toda_group_proof_narrative_renderer.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Public Reference audit"
python ".\phase159_pi3_2_reference_general_form_repair19\audit_phase159_pi3_2_reference_general_form_repair19.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Focused pytest"
python -m pytest -q `
  ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py::test_phase159_r1_6c_toda_51_reference_is_source_faithful" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py::test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

if (Test-Path ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py") {
  Write-Host ""
  Write-Host "[repair18 regression] definition-premise locality"
  python -m pytest -q `
    ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair19 complete"
Write-Host "Repository-wide pytest: NOT RUN (Phase 159 is not finished)"
Write-Host "=============================================================="
