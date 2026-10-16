$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
python -m pytest -q (Join-Path $PSScriptRoot 'test_decoupling.py')
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
Write-Host 'R6-1 reference decoupling completed. Full pytest NOT run.'
