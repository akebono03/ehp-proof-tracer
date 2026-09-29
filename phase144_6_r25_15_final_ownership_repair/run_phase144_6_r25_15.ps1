$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-15 Final Ownership Repair"
Write-Host "R25-13 rollback + semantic contribution identity"
Write-Host "=============================================================="

if (-not (Test-Path ".git")) {
  throw "Run from the ehp-proof-tracer repository root."
}

Write-Host ""
Write-Host "A. Applying final minimal repair..."
python ".\phase144_6_r25_15_final_ownership_repair\apply_phase144_6_r25_15.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_argument_multi_renderer.py" `
  ".\toda_group_proof_narrative_contribution_ordering.py"

Write-Host ""
Write-Host "C. Semantic contribution identity..."
python -m pytest -q `
  ".\phase144_6_r25_15_final_ownership_repair\test_phase144_6_r25_15.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "D. depth=2 definition regression..."
python -m pytest -q `
  ".\tests\test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "E. pi_6^3 generic production route..."
python -m pytest -q `
  ".\tests\test_phase144_6_pi6_generic_production_route.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "F. Six-group final completion invariants..."
python -m pytest -q `
  ".\tests\test_phase144_6_r5_43_11d_final_completion_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Focused Phase 144-6 completion checks: PASS"
Write-Host "Now running the Phase-final full pytest exactly once."
Write-Host "=============================================================="
Write-Host ""

python -m pytest -q
if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "FULL PYTEST: FAIL"
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "FULL PYTEST: PASS"
Write-Host "Phase 144-6 completion test sequence: PASS"
Write-Host "=============================================================="
