$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-R2: R24 rollback + owner diagnosis"
Write-Host "R25 rollback-runner repair only"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Restoring exactly the two pre-R24 production states..."
python (Join-Path $PatchRoot "rollback_r24_r2.py")
if ($LASTEXITCODE -ne 0) {
  throw "R24 rollback failed."
}

Write-Host ""
Write-Host "B. Verifying both production files equal Git HEAD..."
git diff --exit-code -- "main.py"
if ($LASTEXITCODE -ne 0) {
  throw "main.py still differs from Git HEAD."
}

git diff --exit-code -- "toda_group_proof_narrative_argument_multi_renderer.py"
if ($LASTEXITCODE -ne 0) {
  throw "multi renderer still differs from Git HEAD."
}

Write-Host "Both R24 production changes are fully rolled back."

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
  Write-Host "R25-R2 diagnosis completed."
  Write-Host "Production changes after rollback: NONE versus Git HEAD."
  Write-Host "Full suite intentionally not run."
  Write-Host "STOP: inspect owner diagnosis before any repair."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
