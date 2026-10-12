$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$env:PYTHONPATH = $Root
python -m py_compile '.\phase165_r5_manifest_bridge.py' '.\phase165_r5_manifest_bridge\audit.py' '.\tests\test_phase165_r5_manifest_bridge.py'
if ($LASTEXITCODE -ne 0) { throw 'R5 compile failed' }
python -m pytest -q '.\tests\test_phase165_r5_manifest_bridge.py'
if ($LASTEXITCODE -ne 0) { throw 'R5 focused tests failed' }
python '.\phase165_r5_manifest_bridge\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R5 audit failed' }
Write-Host 'Phase 165 R5 source-order bridge verified; full pytest NOT run.'
