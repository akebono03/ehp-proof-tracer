$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-16 Depth=2 Derivation Support Repair"
Write-Host "Scope: CLI depth=2 derivation connector only"
Write-Host "=============================================================="

if (-not (Test-Path ".git")) {
  throw "Run from the ehp-proof-tracer repository root."
}

Write-Host ""
Write-Host "A. Applying R25-16..."
python ".\phase144_6_r25_16_depth2_derivation_support_repair\apply_phase144_6_r25_16.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_argument_body_renderer.py" `
  ".\toda_group_proof_narrative_contribution_ordering.py"

Write-Host ""
Write-Host "C. New depth=2 connector regression..."
python -m pytest -q `
  ".\phase144_6_r25_16_depth2_derivation_support_repair\test_phase144_6_r25_16.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "D. Existing depth=2 definition regression..."
python -m pytest -q `
  ".\tests\test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "E. Existing pi_6^3 generic production route..."
python -m pytest -q `
  ".\tests\test_phase144_6_pi6_generic_production_route.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "F. Existing derivation connector regressions..."
python -m pytest -q `
  ".\tests\test_phase143_57c_step_derivation_connector.py" `
  ".\tests\test_phase143_61b_direct_premise_narrative.py" `
  ".\tests\test_phase144_6_r25_9a_r1_relocation_hidden.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "R25-16 focused tests: PASS"
Write-Host "Full pytest intentionally NOT run yet."
Write-Host "=============================================================="
