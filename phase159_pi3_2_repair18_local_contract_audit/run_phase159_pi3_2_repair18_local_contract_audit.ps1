$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 pi3_2 repair18 local contract audit"
Write-Host "No production changes"
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

  Write-Host "[1/2] Print repair18 expected constants and actual paragraphs"
  python ".\phase159_pi3_2_repair18_local_contract_audit\audit_phase159_pi3_2_repair18_local_contract.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "[2/2] Re-run repair18 locality tests"
  python -m pytest -q `
    ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
  if ($LASTEXITCODE -eq 0) {
    Write-Host "repair18 locality tests already pass."
  }
  else {
    Write-Host "repair18 locality failures reproduced."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Audit complete"
  Write-Host "Production changes: NONE"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}
