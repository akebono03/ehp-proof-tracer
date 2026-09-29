$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R5 Full-Depth +2 Ownership Delta Audit"
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
    ".\phase144_6_r25_11_r5_full_depth_plus2_ownership_delta_audit\audit_r25_11_r5.py" `
    ".\phase144_6_r25_11_r5_full_depth_plus2_ownership_delta_audit\test_phase144_6_r25_11_r5.py"

  Write-Host ""
  Write-Host "B. Lightweight audit-contract tests..."
  pytest -q `
    ".\phase144_6_r25_11_r5_full_depth_plus2_ownership_delta_audit\test_phase144_6_r25_11_r5.py"

  Write-Host ""
  Write-Host "C. Cached six-group ownership delta audit..."
  python `
    ".\phase144_6_r25_11_r5_full_depth_plus2_ownership_delta_audit\audit_r25_11_r5.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R5 completed."
  Write-Host "Please paste the complete A-D audit output."
  Write-Host "No production files were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  Pop-Location
}
