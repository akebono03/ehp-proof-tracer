param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -m pytest -q phase175_r4r12r3_candidate_diagnostic/tests/test_diagnose.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R3 focused tests failed' }
python -m phase175_r4r12r3_candidate_diagnostic.diagnose --root $root
if ($LASTEXITCODE -ne 0) { throw 'R4R12R3 diagnostic failed' }
