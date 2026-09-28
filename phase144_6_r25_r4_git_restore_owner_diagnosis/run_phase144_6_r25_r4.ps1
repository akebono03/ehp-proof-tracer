$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-R4: exact Git rollback + owner diagnosis"
Write-Host "No string-based production rewriting"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Restoring the two R24 production files exactly from HEAD..."
git restore --source=HEAD -- `
  "main.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py"

if ($LASTEXITCODE -ne 0) {
  throw "git restore failed."
}

Write-Host ""
Write-Host "B. Verifying exact HEAD equality..."
git diff --exit-code -- `
  "main.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py"

if ($LASTEXITCODE -ne 0) {
  throw "R24 production files still differ from HEAD."
}

Write-Host "R24 rollback verified: both production files exactly match HEAD."

Write-Host ""
Write-Host "Current production status:"
git status --short -- `
  "main.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py"

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "C. Running focused pre-diagnosis tests..."
  pytest -q `
    "tests/test_phase144_6_pi6_generic_production_route.py" `
    "tests/test_phase144_5_generic_definition_order_equations.py" `
    "tests/test_phase143_61b_r_semantic_suppression_priority.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Focused pre-diagnosis tests failed."
  }

  Write-Host ""
  Write-Host "D. Running step-identity owner diagnosis..."
  python (Join-Path $PatchRoot "diagnose_phase144_6_r25.py")

  if ($LASTEXITCODE -ne 0) {
    throw "Owner diagnosis failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-R4 diagnosis completed."
  Write-Host "R24 production changes: fully removed."
  Write-Host "New production repair: none."
  Write-Host "Full suite intentionally not run."
  Write-Host "STOP: inspect diagnosis before any repair."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
