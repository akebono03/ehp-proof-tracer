$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path

try {
  Write-Host "=============================================================================="
  Write-Host "Phase 143-75AB Whitehead correction semantic pre-audit"
  Write-Host "=============================================================================="

  $oldAudit = Get-ChildItem `
    -Path ".\phase143_75z" `
    -Filter "audit_phase143_75z*.py" `
    -File `
    -ErrorAction Stop |
    Select-Object -First 1

  Write-Host ""
  Write-Host "[1] Confirm unchanged 112-group / 11033-node population"
  python $oldAudit.FullName
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "[2] Inspect TodaLemma54WhiteheadCorrectionDataStatement first-class fields"
  python -c "from dataclasses import fields; from test_phase60_nu4_whitehead_correction import build_phase60_8_data; from toda_proof_narrative_renderer import render_toda_proof_statement_latex; s=build_phase60_8_data()['whitehead_data_step'].conclusion; print('type:',type(s).__name__); print('fields:',tuple(f.name for f in fields(s))); [print(f.name+':',type(getattr(s,f.name)).__name__,repr(getattr(s,f.name))) for f in fields(s)]; print('current semantic rendering:',render_toda_proof_statement_latex(s))"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "No implementation changes were made."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
