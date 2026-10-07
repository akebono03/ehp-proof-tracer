$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 repair18 numbered-locality repair23"
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

  Write-Host "[1/7] Apply repair23"
  python ".\phase159_pi3_2_repair18_numbered_locality_repair23\apply_phase159_pi3_2_repair18_numbered_locality_repair23.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[2/7] Syntax check"
  python -m py_compile `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[3/7] pi3_2 locality audit"
  python ".\phase159_pi3_2_repair18_numbered_locality_repair23\audit_phase159_pi3_2_repair18_numbered_locality_repair23.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[4/7] repair18 locality tests"
  python -m pytest -q `
    ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[5/7] numbered-reasoning regression"
  python -m pytest -q `
    ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[6/7] R1-6d Reference/linkage regression"
  python -m pytest -q `
    ".\tests\test_phase159_r1_6d_specialization_reference_linkage_finalization.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[7/7] Reference component regression"
  python -m pytest -q `
    ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py::test_phase159_r1_6c_toda_51_reference_is_source_faithful" `
    ".\tests\test_phase159_r1_6b_toda51_attribution.py::test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair23 complete"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
