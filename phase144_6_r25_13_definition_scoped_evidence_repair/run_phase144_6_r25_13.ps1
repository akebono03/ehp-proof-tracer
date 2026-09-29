$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-13 Definition-scoped Evidence Repair"
Write-Host "Minimal production change: one ownership boundary"
Write-Host "=============================================================="

if (-not (Test-Path ".git")) {
    throw "Run this script from the ehp-proof-tracer repository root."
}

Write-Host ""
Write-Host "A. Preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_argument_multi_renderer.py"

Write-Host ""
Write-Host "B. Applying minimal production repair..."
python `
  ".\phase144_6_r25_13_definition_scoped_evidence_repair\apply_phase144_6_r25_13.py"

Write-Host ""
Write-Host "C. Syntax check after repair..."
python -m py_compile `
  ".\toda_group_proof_narrative_argument_multi_renderer.py"

Write-Host ""
Write-Host "D. R25-13 ownership-boundary test..."
python -m pytest -q `
  ".\phase144_6_r25_13_definition_scoped_evidence_repair\test_phase144_6_r25_13.py"

Write-Host ""
Write-Host "E. Existing depth=2 definition regression tests..."
python -m pytest -q `
  ".\tests\test_phase144_6_r25_9b_nu_prime_definition_depth2.py"

Write-Host ""
Write-Host "F. Existing generic production-route tests..."
python -m pytest -q `
  ".\tests\test_phase144_6_pi6_generic_production_route.py"

Write-Host ""
Write-Host "G. Existing final-completion focused audit tests..."
python -m pytest -q `
  ".\tests\test_phase144_6_r5_43_11d_final_completion_audit.py"

Write-Host ""
Write-Host "=============================================================="
Write-Host "R25-13 focused verification complete."
Write-Host "Full pytest is intentionally NOT run here."
Write-Host "=============================================================="
