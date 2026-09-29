$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here
$Output = Join-Path $Here "r25_25_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-25 Ownership Pipeline Diagnosis"
Write-Host "Rollback R25-24 experiment, then diagnose only"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Rolling back rejected R25-24 production experiment..."
  python `
    ".\phase144_6_r25_25_ownership_pipeline_diagnosis\rollback_phase144_6_r25_24.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-24 rollback failed."
  }
  Write-Host ""

  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_method_evidence.py" `
    ".\toda_group_proof_narrative_argument_multi_renderer.py" `
    ".\phase144_6_r25_25_ownership_pipeline_diagnosis\audit_phase144_6_r25_25.py" `
    ".\phase144_6_r25_25_ownership_pipeline_diagnosis\test_phase144_6_r25_25.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-25 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "C. Rollback/pipeline focused tests..."
  pytest -q `
    ".\phase144_6_r25_25_ownership_pipeline_diagnosis\test_phase144_6_r25_25.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-25 focused tests failed."
  }
  Write-Host ""

  Write-Host "D. Existing method-evidence and generic-route regressions..."
  pytest -q `
    ".\tests\test_phase143_19_method_evidence.py" `
    ".\tests\test_phase143_22_exactness_components.py" `
    ".\tests\test_phase143_39_exactness_contribution_ownership.py" `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-25 regression checks failed."
  }
  Write-Host ""

  Write-Host "E. Six-group ownership-pipeline diagnosis..."
  python `
    ".\phase144_6_r25_25_ownership_pipeline_diagnosis\audit_phase144_6_r25_25.py" |
    Tee-Object `
      -FilePath $Output
  if ($LASTEXITCODE -ne 0) {
    throw "R25-25 diagnosis failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-25 diagnosis completed."
  Write-Host "Output:"
  Write-Host "  $Output"
  Write-Host "R25-24 experimental production change is rolled back."
  Write-Host "No new production behavior was added."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
