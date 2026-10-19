$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'patch.py')
if ($LASTEXITCODE -ne 0) { throw 'Web route alignment patch failed' }
python -m pytest -q test_phase165_r52_r4_flask_connection.py test_phase165_r52_r5_auto_search.py test_phase165_r52_r8_show_proof_route.py
if ($LASTEXITCODE -ne 0) { throw 'Web route alignment targeted pytest failed' }
Write-Host 'Web route alignment targeted PASS; full pytest NOT run'
