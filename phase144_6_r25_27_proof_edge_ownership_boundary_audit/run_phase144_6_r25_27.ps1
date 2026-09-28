$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here
$Output = Join-Path $Here "r25_27_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-27 Proof-Edge Ownership Boundary Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase144_6_r25_27_proof_edge_ownership_boundary_audit\audit_phase144_6_r25_27.py" `
    ".\phase144_6_r25_27_proof_edge_ownership_boundary_audit\test_phase144_6_r25_27.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-27 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "B. Focused audit-contract tests..."
  pytest -q `
    ".\phase144_6_r25_27_proof_edge_ownership_boundary_audit\test_phase144_6_r25_27.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-27 focused audit-contract tests failed."
  }
  Write-Host ""

  Write-Host "C. Existing argument-local-body regressions..."
  pytest -q `
    ".\tests\test_phase143_41_argument_local_body.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-27 local-body regressions failed."
  }
  Write-Host ""

  Write-Host "D. Six-group direct-premise ownership audit..."
  python `
    ".\phase144_6_r25_27_proof_edge_ownership_boundary_audit\audit_phase144_6_r25_27.py" |
    Tee-Object `
      -FilePath $Output
  if ($LASTEXITCODE -ne 0) {
    throw "R25-27 diagnosis failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-27 diagnosis completed."
  Write-Host "Output:"
  Write-Host "  $Output"
  Write-Host "No production files were changed."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
