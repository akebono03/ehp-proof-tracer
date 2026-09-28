$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-R5: owner diagnosis after confirmed rollback"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Verifying R24 production files still exactly match HEAD..."
git diff --exit-code -- `
  "main.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py"

if ($LASTEXITCODE -ne 0) {
  throw "Production files differ from HEAD. Diagnosis aborted."
}

Write-Host "Confirmed: both R24 production files exactly match HEAD."

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "B. Reproducing the known depth=2 regression..."
  pytest -q `
    "tests/test_phase144_6_pi6_generic_production_route.py::test_phase144_6_cli_pi6_3_narrative_uses_generic_route"
  $KnownRegressionExitCode = $LASTEXITCODE

  if ($KnownRegressionExitCode -eq 0) {
    Write-Host "WARNING: known depth=2 regression unexpectedly passed."
  }
  else {
    Write-Host "Known depth=2 regression reproduced; continuing diagnosis."
  }

  Write-Host ""
  Write-Host "C. Running unaffected focused controls..."
  pytest -q `
    "tests/test_phase144_5_generic_definition_order_equations.py" `
    "tests/test_phase143_61b_r_semantic_suppression_priority.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Unaffected focused controls failed."
  }

  Write-Host ""
  Write-Host "D. Running corrected production-order owner diagnosis..."
  python (Join-Path $PatchRoot "diagnose_phase144_6_r25_r5.py")

  if ($LASTEXITCODE -ne 0) {
    throw "Owner diagnosis failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-R5 diagnosis completed."
  Write-Host "Production changes: none."
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
