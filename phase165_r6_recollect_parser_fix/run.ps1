$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r52_r4_flask_bridge.py'))) { throw 'Run from the ehp_proof repository root.' }
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
python -m pytest -q .\phase165_r6_recollect_parser_fix\tests\test_repair.py
if ($LASTEXITCODE -ne 0) { throw 'Targeted parser tests failed. Report not modified.' }
python .\phase165_r6_recollect_parser_fix\repair.py --root "$root"
if ($LASTEXITCODE -ne 0) { throw 'Report repair failed; inspect existing report.' }
Write-Host 'Existing log re-parsed. No pytest collection or test-body execution performed.'
