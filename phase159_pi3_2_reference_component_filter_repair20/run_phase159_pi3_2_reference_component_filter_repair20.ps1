$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 Reference component-filter repair20"
Write-Host "Use existing fixed-statement component selection"
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

  Write-Host "[1/5] Apply repair20"
  python ".\phase159_pi3_2_reference_component_filter_repair20\apply_phase159_pi3_2_reference_component_filter_repair20.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[2/5] Syntax check"
  python -m py_compile `
    ".\toda_group_proof_narrative_references.py" `
    ".\toda_group_proof_narrative_contribution_renderer.py" `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[3/5] Reference audit"
  python ".\phase159_pi3_2_reference_component_filter_repair20\audit_phase159_pi3_2_reference_component_filter_repair20.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[4/5] Focused Reference tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py::test_phase159_r1_6c_toda_51_reference_is_source_faithful" `
    ".\tests\test_phase159_r1_6b_toda51_attribution.py::test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[5/5] repair18 regression"
  if (Test-Path ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py") {
    python -m pytest -q `
      ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
    if ($LASTEXITCODE -ne 0) {
      exit $LASTEXITCODE
    }
  }
  else {
    Write-Host "repair18 locality test file not present; skipped."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair20 complete"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
