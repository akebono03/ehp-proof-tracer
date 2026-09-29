$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R4 Closure-Origin Boundary Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONUTF8 = "1"

  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase144_6_r25_11_r4_closure_origin_boundary_audit\audit_r25_11_r4.py" `
    ".\phase144_6_r25_11_r4_closure_origin_boundary_audit\test_phase144_6_r25_11_r4_closure_origin_boundary.py"

  Write-Host ""
  Write-Host "B. Focused closure-origin identity tests..."
  pytest -q `
    ".\phase144_6_r25_11_r4_closure_origin_boundary_audit\test_phase144_6_r25_11_r4_closure_origin_boundary.py"

  Write-Host ""
  Write-Host "C. Closure-origin boundary audit..."
  python `
    ".\phase144_6_r25_11_r4_closure_origin_boundary_audit\audit_r25_11_r4.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R4 completed."
  Write-Host "Please paste the complete A-C output."
  Write-Host "No production files were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  Pop-Location
}
