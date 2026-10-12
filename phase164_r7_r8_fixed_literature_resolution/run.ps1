$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python ".\phase164_r7_r8_fixed_literature_resolution\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q tests/test_phase164_r7_r8_fixed_literature_resolution.py tests/test_phase164_r7_statement_resolution.py tests/test_phase164_r4_r8_registry_reconstruction.py tests/test_phase164_r4_r6_typed_binding.py tests/test_phase164_r3_registry_search_connection.py tests/test_phase164_r2_citation_eligibility.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 164 R7-R8 focused tests PASS; full pytest NOT run."
