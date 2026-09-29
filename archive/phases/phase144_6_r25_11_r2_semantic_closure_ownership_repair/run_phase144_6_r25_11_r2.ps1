$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R2 Semantic Closure Ownership Repair"
Write-Host "Restore general direct-premise frontier protection"
Write-Host "=============================================================="

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONUTF8 = "1"

  Write-Host ""
  Write-Host "A. Applying minimal production repair..."
  python ".\phase144_6_r25_11_r2_semantic_closure_ownership_repair\apply_phase144_6_r25_11_r2.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_argument_multi_renderer.py" `
    ".\phase144_6_r25_11_r2_semantic_closure_ownership_repair\test_phase144_6_r25_11_r2.py"

  Write-Host ""
  Write-Host "C. R25-11-R2 focused ownership-boundary tests..."
  pytest -q ".\phase144_6_r25_11_r2_semantic_closure_ownership_repair\test_phase144_6_r25_11_r2.py"

  Write-Host ""
  Write-Host "D. R5-37 through R5-40 population regressions..."
  pytest -q `
    ".\tests\test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py" `
    ".\tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py" `
    ".\tests\test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py" `
    ".\tests\test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py"

  Write-Host ""
  Write-Host "E. Participation, detached, completion, connector regressions..."
  pytest -q `
    ".\tests\test_phase144_6_r5_43_3.py" `
    ".\tests\test_phase144_6_r5_43_11c_r2_argument_participation_guard.py" `
    ".\tests\test_phase144_6_r5_43_11d_final_completion_audit.py"

  Write-Host ""
  Write-Host "F. R25-9B depth=2 semantic closure regression..."
  pytest -q ".\phase144_6_r25_9b_nu_prime_definition_depth2_selection_repair\test_phase144_6_r25_9b_nu_prime_definition_depth2.py"

  Write-Host ""
  Write-Host "G. R25-10 ownership audit with UTF-8 output..."
  powershell -ExecutionPolicy Bypass `
    -File ".\phase144_6_r25_10_r5_argument_api_audit_repair\run_phase144_6_r25_10_r5.ps1"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R2 focused verification completed."
  Write-Host "No full test suite was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  Pop-Location
}
