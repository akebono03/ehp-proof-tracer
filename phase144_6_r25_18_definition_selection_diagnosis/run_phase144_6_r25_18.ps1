$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-18 Definition Selection Diagnosis"
Write-Host "Production changes: NONE"
Write-Host "=============================================================="

if (-not (Test-Path ".git")) {
  throw "Run from the ehp-proof-tracer repository root."
}

python ".\phase144_6_r25_18_definition_selection_diagnosis\diagnose_phase144_6_r25_18.py" |
  Tee-Object `
    -FilePath ".\phase144_6_r25_18_definition_selection_diagnosis\r25_18_output.txt"
