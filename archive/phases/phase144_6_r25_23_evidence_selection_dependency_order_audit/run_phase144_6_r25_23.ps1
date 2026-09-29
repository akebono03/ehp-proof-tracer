$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here
$Output = Join-Path $Here "r25_23_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-23 Narrative Evidence / Dependency Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\audit_phase144_6_r25_23.py" `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\test_phase144_6_r25_23.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "B. Focused audit-contract tests..."
  pytest -q `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\test_phase144_6_r25_23.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23 focused audit-contract tests failed."
  }
  Write-Host ""

  Write-Host "C. Six-group evidence-selection / dependency-order audit..."
  python `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\audit_phase144_6_r25_23.py" |
    Tee-Object `
      -FilePath $Output
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23 audit failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-23 audit completed."
  Write-Host "Output:"
  Write-Host "  $Output"
  Write-Host "Production changes: none."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
