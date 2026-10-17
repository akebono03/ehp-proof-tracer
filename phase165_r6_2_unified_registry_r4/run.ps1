$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -m pytest -q .\phase165_r6_2_unified_registry_r4\test_r4_audit.py
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
python -m phase165_r6_2_unified_registry_r4.r4_audit --root $root --out .\phase165_r6_2_unified_registry_r4\reports
if ($LASTEXITCODE -ne 0) { throw 'R4 audit failed' }
Write-Output 'R4 applicability audit completed; production unchanged; full pytest NOT run.'
