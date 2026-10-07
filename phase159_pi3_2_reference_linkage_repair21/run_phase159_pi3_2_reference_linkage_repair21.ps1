$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 reference-linkage repair21"
Write-Host "Reuse existing specialized linkage; display general Reference"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PreviousPythonPath = $env:PYTHONPATH
$PathSeparator = [System.IO.Path]::PathSeparator

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = [string]::Concat(
    $RepoRoot,
    $PathSeparator,
    $PreviousPythonPath
  )
}

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/6] Apply repair21"
  python ".\phase159_pi3_2_reference_linkage_repair21\apply_phase159_pi3_2_reference_linkage_repair21.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[2/6] Syntax check"
  python -m py_compile `
    ".\toda_group_proof_narrative_contribution_renderer.py" `
    ".\toda_group_proof_narrative_references.py" `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[3/6] Reference/linkage audit"
  python ".\phase159_pi3_2_reference_linkage_repair21\audit_phase159_pi3_2_reference_linkage_repair21.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[4/6] Reference focused tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py::test_phase159_r1_6c_toda_51_reference_is_source_faithful" `
    ".\tests\test_phase159_r1_6b_toda51_attribution.py::test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[5/6] R1-6d linkage tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_6d_specialization_reference_linkage_finalization.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[6/6] repair18 locality tests"
  python -m pytest -q `
    ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair21 complete"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
