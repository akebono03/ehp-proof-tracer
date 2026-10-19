$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\test_phase165_r52_r2_search_adapter.py')) { throw 'Run from ehp_proof root.' }
& python '.\phase165_r6_mock_completion_contract_fix\install.py'
if ($LASTEXITCODE -ne 0) { throw "R6 targeted tests failed with exit=$LASTEXITCODE" }
Write-Host 'R6 completion contract targeted PASS; full pytest NOT run'
