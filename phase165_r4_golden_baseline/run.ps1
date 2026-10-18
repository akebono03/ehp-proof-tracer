$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python ".\phase165_r4_golden_baseline\capture_baseline.py"
if ($LASTEXITCODE -ne 0) { throw 'R4 baseline capture / verification failed' }
python -m pytest -q ".\phase165_r4_golden_baseline\tests\test_phase165_r4_golden_baseline.py"
if ($LASTEXITCODE -ne 0) { throw 'R4 regression tests failed' }
Write-Host 'R4 PASS: immutable pi3_2 and pi4_3 baselines; full pytest NOT run'
