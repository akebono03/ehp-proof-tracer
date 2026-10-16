$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -m pytest -q .\phase165_r6_2_unified_registry_r4_r3\test_r4_r3_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R4-3 targeted pytest failed' }
python -m phase165_r6_2_unified_registry_r4_r3.r4_r3_audit --root $root --out .\phase165_r6_2_unified_registry_r4_r3\reports
if ($LASTEXITCODE -ne 0) { throw 'R4-3 provenance audit failed' }
Write-Output 'R4-3 read-only provenance audit completed; full pytest NOT run.'
