$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -m pytest -q .\phase165_r6_2_unified_registry_r3_r4\test_r3_r4.py
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
python -m phase165_r6_2_unified_registry_r3_r4.install
if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
python -c "import phase165_r52_r9_shared_math; print('Shared provider import: PASS')"
if ($LASTEXITCODE -ne 0) { throw 'Import check failed' }
Write-Output 'R3-4 installed; full pytest NOT run.'
