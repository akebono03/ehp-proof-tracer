$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $PSScriptRoot
python -m pytest -q test_apply.py
if ($LASTEXITCODE -ne 0) { throw 'R6-13 package tests failed; no retirement performed' }
Set-Location $root
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R6-13 retirement failed; check the error above' }
Write-Host 'R6-13 completed. Full pytest NOT run.'
