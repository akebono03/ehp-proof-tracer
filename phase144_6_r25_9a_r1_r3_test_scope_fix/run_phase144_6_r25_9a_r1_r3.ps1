$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-9A-R1-R3"
Write-Host "Focused test scope correction only"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Replacing only the over-specified R25-9A-R1 test..."
Copy-Item `
  (Join-Path $PatchRoot "test_phase144_6_r25_9a_r1_relocation_hidden.py") `
  (Join-Path $ProjectRoot "tests\test_phase144_6_r25_9a_r1_relocation_hidden.py") `
  -Force

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "B. Running R25-9A completion focused tests..."
  pytest -q `
    "tests/test_phase144_6_r25_9a_r1_relocation_hidden.py" `
    "tests/test_phase144_6_r25_9a_pi5_suppression.py" `
    "tests/test_phase144_6_r4_supporting_fact_filtering.py" `
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py" `
    "tests/test_phase144_6_r5_15u_evidence_integration.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R25-9A-R1-R3 focused tests failed."
  }

  Write-Host ""
  Write-Host "C. Production diff retained from R25-9A/R1..."
  git diff -- `
    "toda_group_proof_narrative_argument_multi_renderer.py" `
    "toda_group_proof_narrative_argument_body_renderer.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-9A completion focused tests: PASS"
  Write-Host "Production changes in R3: none."
  Write-Host "Full suite intentionally not run."
  Write-Host "Next boundary: R25-9B nu-prime depth=2 selection."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}
