$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $PSScriptRoot 'tests\test_cleanup.py')
if ($LASTEXITCODE -ne 0) { throw 'Cleanup safety tests failed.' }
python (Join-Path $PSScriptRoot 'cleanup.py') $root
if ($LASTEXITCODE -ne 0) { throw 'Cleanup failed.' }
