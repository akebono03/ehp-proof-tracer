$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q tests/test_phase164_r7_statement_resolution.py tests/test_phase164_r3_registry_search_connection.py tests/test_phase164_r2_citation_eligibility.py tests/test_phase163_r4_registry_bridge.py tests/test_phase163_r2_unified_registry.py tests/test_proof_repository.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 164 R7 focused tests PASS; full pytest NOT run.'
