$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python -m pytest -q "$PSScriptRoot\test_apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R6-18 package tests failed; no retirement' }
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R6-18 retirement blocked; see report.json' }
Write-Host 'R6-18 retired historic test functions; full pytest NOT run.'
