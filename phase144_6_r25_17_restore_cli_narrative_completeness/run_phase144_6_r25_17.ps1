$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-17 Restore CLI Narrative Completeness"
Write-Host "Rollback R25-16; restore previously validated R24 CLI boundary"
Write-Host "=============================================================="

if (-not (Test-Path ".git")) {
  throw "Run from the ehp-proof-tracer repository root."
}

Write-Host ""
Write-Host "A. Applying R25-17..."
python ".\phase144_6_r25_17_restore_cli_narrative_completeness\apply_phase144_6_r25_17.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\main.py" `
  ".\toda_group_proof_narrative_argument_body_renderer.py"

Write-Host ""
Write-Host "C. R25-17 CLI depth=2 Narrative completeness..."
python -m pytest -q `
  ".\phase144_6_r25_17_restore_cli_narrative_completeness\test_phase144_6_r25_17.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "D. Existing depth=2 semantic-closure contract..."
python -m pytest -q `
  ".\tests\test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "E. Existing pi_6^3 generic production route..."
python -m pytest -q `
  ".\tests\test_phase144_6_pi6_generic_production_route.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "F. Existing generic derivation regressions..."
python -m pytest -q `
  ".\tests\test_phase143_57c_step_derivation_connector.py" `
  ".\tests\test_phase143_61b_direct_premise_narrative.py" `
  ".\tests\test_phase144_6_r25_9a_r1_relocation_hidden.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "R25-17 focused completion checks: PASS"
Write-Host "No additional audit is scheduled."
Write-Host "Full pytest intentionally NOT run in this runner."
Write-Host "=============================================================="
