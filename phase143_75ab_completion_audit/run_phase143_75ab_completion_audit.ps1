$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  Write-Host "=============================================================================="
  Write-Host "Phase 143-75AB completion audit"
  Write-Host "=============================================================================="

  $inventoryCandidates = @(
    ".\phase143_75u\audit_phase143_75u_remaining_fallbacks.py",
    ".\phase143_75u\audit_phase143_75u.py"
  )

  $inventory = $null
  foreach ($candidate in $inventoryCandidates) {
    if (Test-Path $candidate) {
      $inventory = $candidate
      break
    }
  }

  if ($null -eq $inventory) {
    throw "Could not locate the Phase 143-75U remaining-fallback audit."
  }

  Write-Host ("inventory audit: " + $inventory)
  python $inventory
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "[Focused semantic rendering]"
  python -c "from test_phase60_nu4_whitehead_correction import build_phase60_8_data; from toda_proof_narrative_renderer import render_toda_proof_statement_latex; s=build_phase60_8_data()['whitehead_data_step'].conclusion; print('type:', type(s).__name__); print('rendering:', render_toda_proof_statement_latex(s))"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected completion signals:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  rule-name fallback occurrences: 236"
  Write-Host "  TodaLemma54WhiteheadCorrectionDataStatement absent from remaining inventory"
  Write-Host "  Toda Lemma 5.4 Whitehead correction data absent from fallback rule-name inventory"
  Write-Host "  focused rendering is non-None semantic mathematics"
  Write-Host ""
  Write-Host "No source files were changed."
  Write-Host "No pytest was run."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
