$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"
try {
  Write-Host "=============================================================================="
  Write-Host "Phase 143-75AC completion audit"
  Write-Host "=============================================================================="

  python ".\phase143_75u\audit_phase143_75u_remaining_fallbacks.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "[Focused semantic rendering]"
  python -c "from test_phase60_toda48_hopf_parity import build_phase60_7_data; from toda_proof_narrative_renderer import render_toda_proof_statement_latex; s=build_phase60_7_data()['final_step'].conclusion; print('type:', type(s).__name__); print('rendering:', render_toda_proof_statement_latex(s))"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected completion signals:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  rule-name fallback occurrences: 216"
  Write-Host "  TodaLemma54HopfOddMultipleStatement absent from remaining inventory"
  Write-Host "  Toda 4.8 Lemma 5.4 Hopf odd multiple absent from fallback inventory"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No source files were changed."
  Write-Host "No pytest was run."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
