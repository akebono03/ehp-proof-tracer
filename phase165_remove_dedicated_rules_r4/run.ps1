$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'standard_production_applicability_catalog.py'))) { throw 'Run from ehp_proof repository root.' }
$env:PYTHONPATH = $root + [IO.Path]::PathSeparator + $env:PYTHONPATH
python .\phase165_remove_dedicated_rules_r4\remove.py
if ($LASTEXITCODE -ne 0) { throw 'Removal blocked. Inspect report. No changes on validation failure.' }
python -m pytest -q .\phase165_remove_dedicated_rules_r4\test_remove.py
if ($LASTEXITCODE -ne 0) { throw 'Targeted verification failed.' }
Write-Output 'Phase165 dedicated rules removal checked; full pytest NOT run.'
