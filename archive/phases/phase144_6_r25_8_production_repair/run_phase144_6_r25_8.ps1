$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-8 production repair"
Write-Host "Minimal nu-prime provenance repair"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying minimal production repair..."
python (Join-Path $PatchRoot "apply_phase144_6_r25_8.py")
if ($LASTEXITCODE -ne 0) {
  throw "R25-8 apply failed."
}

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "B. Running R25-8 focused regression tests..."
  pytest -q `
    "tests/test_phase144_6_r25_8_depth2_definition_provenance.py" `
    "tests/test_phase144_6_pi6_generic_production_route.py" `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
    "tests/test_phase144_5_generic_definition_order_equations.py" `
    "tests/test_phase58_nu_prime_specialization.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py" `
    "tests/test_phase143_61b_r_semantic_suppression_priority.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R25-8 focused tests failed."
  }

  Write-Host ""
  Write-Host "C. Showing production diff..."
  git diff -- `
    "toda_upstream_bootstrap.py" `
    "tests/test_phase144_6_r25_8_depth2_definition_provenance.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-8 focused repair completed."
  Write-Host "Full suite intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
