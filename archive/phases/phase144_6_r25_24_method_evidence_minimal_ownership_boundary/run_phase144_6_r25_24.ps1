$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here
$Output = Join-Path $Here "r25_24_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-24 Method Evidence Minimal Ownership Boundary"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Applying minimal production repair..."
  python `
    ".\phase144_6_r25_24_method_evidence_minimal_ownership_boundary\apply_phase144_6_r25_24.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-24 production repair failed."
  }
  Write-Host ""

  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_method_evidence.py" `
    ".\toda_group_proof_narrative_argument_multi_renderer.py" `
    ".\phase144_6_r25_24_method_evidence_minimal_ownership_boundary\test_phase144_6_r25_24.py" `
    ".\phase144_6_r25_24_method_evidence_minimal_ownership_boundary\audit_phase144_6_r25_24.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-24 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "C. R25-24 focused tests..."
  pytest -q `
    ".\phase144_6_r25_24_method_evidence_minimal_ownership_boundary\test_phase144_6_r25_24.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-24 focused tests failed."
  }
  Write-Host ""

  Write-Host "D. Existing method-evidence/component regressions..."
  pytest -q `
    ".\tests\test_phase143_19_method_evidence.py" `
    ".\tests\test_phase143_22_exactness_components.py" `
    ".\tests\test_phase143_26_exactness_relevance.py" `
    ".\tests\test_phase143_28_exactness_selection.py" `
    ".\tests\test_phase143_36_argument_body_blocks.py" `
    ".\tests\test_phase143_39_exactness_contribution_ownership.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-24 existing exactness regressions failed."
  }
  Write-Host ""

  Write-Host "E. Existing generic pi6 production-route regression..."
  pytest -q `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-24 generic pi6 regression failed."
  }
  Write-Host ""

  Write-Host "F. Six-group ownership-count audit..."
  python `
    ".\phase144_6_r25_24_method_evidence_minimal_ownership_boundary\audit_phase144_6_r25_24.py" |
    Tee-Object `
      -FilePath $Output
  if ($LASTEXITCODE -ne 0) {
    throw "R25-24 ownership-count audit failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-24 checks completed."
  Write-Host "Output:"
  Write-Host "  $Output"
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
