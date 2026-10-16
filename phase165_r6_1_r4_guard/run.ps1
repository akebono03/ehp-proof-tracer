$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python -m pytest -q (Join-Path $PSScriptRoot 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Focused audit tests failed' }
python (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Remaining-path audit failed' }
Write-Host 'R6-1 remaining entry audit completed; full pytest NOT run.'
