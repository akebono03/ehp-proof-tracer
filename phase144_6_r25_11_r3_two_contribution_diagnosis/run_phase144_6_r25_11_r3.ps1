$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R3 Two-Contribution Diagnosis"
Write-Host "Rollback R25-11-R2, then inspect the 192 vs 190 boundary"
Write-Host "=============================================================="

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONUTF8 = "1"

  Write-Host ""
  Write-Host "A. Rolling back rejected R25-11-R2 production change..."
  python `
    ".\phase144_6_r25_11_r3_two_contribution_diagnosis\rollback_r25_11_r2.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_argument_multi_renderer.py" `
    ".\phase144_6_r25_11_r3_two_contribution_diagnosis\audit_r25_11_r3.py"

  Write-Host ""
  Write-Host "C. Confirming rollback returned the lightweight selected population..."
  python `
    ".\phase144_6_r25_11_r3_two_contribution_diagnosis\audit_r25_11_r3.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R3 completed."
  Write-Host "Please paste the complete A-C output."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  Pop-Location
}
