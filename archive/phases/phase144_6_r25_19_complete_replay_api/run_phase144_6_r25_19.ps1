$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-19 Complete Replay API"
Write-Host "Minimal replay API extension + Narrative integration"
Write-Host "=============================================================="

if (-not (Test-Path ".git")) {
  throw "Run from the ehp-proof-tracer repository root."
}

Write-Host ""
Write-Host "A. Applying R25-19..."
python ".\phase144_6_r25_19_complete_replay_api\apply_phase144_6_r25_19.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\toda_group_result_proof_replay.py" `
  ".\main.py"

Write-Host ""
Write-Host "C. Complete replay API contract..."
python -m pytest -q `
  ".\phase144_6_r25_19_complete_replay_api\test_phase144_6_r25_19_complete_replay_api.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "D. Existing Phase 131 replay API regressions..."
python -m pytest -q `
  ".\tests\test_phase131_3_group_result_proof_replay.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "E. R25-19 CLI Narrative completeness..."
python -m pytest -q `
  ".\phase144_6_r25_19_complete_replay_api\test_phase144_6_r25_19_cli.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "F. Existing depth=2 semantic-closure contract..."
python -m pytest -q `
  ".\tests\test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "G. Existing pi_6^3 generic production route..."
python -m pytest -q `
  ".\tests\test_phase144_6_pi6_generic_production_route.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "R25-19 focused tests: PASS"
Write-Host "Full pytest intentionally NOT run."
Write-Host "=============================================================="

Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
