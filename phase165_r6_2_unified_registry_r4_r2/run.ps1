$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -m pytest -q .\phase165_r6_2_unified_registry_r4_r2\test_r4_r2_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R4-2 targeted pytest failed' }
python -m phase165_r6_2_unified_registry_r4_r2.r4_r2_audit --root $root --out .\phase165_r6_2_unified_registry_r4_r2\reports
if ($LASTEXITCODE -ne 0) { throw 'R4-2 audit failed' }
Write-Output 'R4-2 read-only attribution completed; full pytest NOT run.'
