$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 numbered exactness-prefix repair22"
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

  Write-Host "[1/6] Apply repair22"
  python ".\phase159_pi3_2_numbered_exactness_prefix_repair22\apply_phase159_pi3_2_numbered_exactness_prefix_repair22.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[2/6] Syntax check"
  python -m py_compile `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[3/6] pi3_2 public audit"
  python ".\phase159_pi3_2_numbered_exactness_prefix_repair22\audit_phase159_pi3_2_numbered_exactness_prefix_repair22.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[4/6] Current numbered-reasoning tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[5/6] R1-6d linkage/centered regression"
  python -m pytest -q `
    ".\tests\test_phase159_r1_6d_specialization_reference_linkage_finalization.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[6/6] repair18 locality regression"
  python -m pytest -q `
    ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair22 complete"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
