$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here
$AuditDir = Join-Path $Repo "phase144_6_r25_23_evidence_selection_dependency_order_audit"
$Output = Join-Path $AuditDir "r25_23_output.txt"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-23-R2 Audit Harness Import/API Repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Applying audit-harness-only repair..."
  python `
    ".\phase144_6_r25_23_r2_audit_harness_import_api_repair\repair_phase144_6_r25_23_r2.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23-R2 audit harness repair failed."
  }
  Write-Host ""

  Write-Host "B. Import/API preflight..."
  python -c "from phase144_6_r25_23_evidence_selection_dependency_order_audit.audit_phase144_6_r25_23 import _data; p,b,s,a,m = _data(3,3); assert p and b and s and a and m; print('R25-23 data-construction preflight: PASS')"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23-R2 data-construction preflight failed."
  }
  Write-Host ""

  Write-Host "C. Syntax preflight..."
  python -m py_compile `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\audit_phase144_6_r25_23.py" `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\test_phase144_6_r25_23.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23-R2 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "D. Focused audit-contract tests..."
  pytest -q `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\test_phase144_6_r25_23.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23-R2 focused audit-contract tests failed."
  }
  Write-Host ""

  Write-Host "E. Six-group evidence-selection / dependency-order audit..."
  python `
    ".\phase144_6_r25_23_evidence_selection_dependency_order_audit\audit_phase144_6_r25_23.py" |
    Tee-Object `
      -FilePath $Output
  if ($LASTEXITCODE -ne 0) {
    throw "R25-23-R2 six-group audit failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-23-R2 audit completed."
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
