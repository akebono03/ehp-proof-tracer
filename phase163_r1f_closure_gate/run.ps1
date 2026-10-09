$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$env:PYTHONPATH = $PSScriptRoot
python -B -m pytest -q (Join-Path $PSScriptRoot 'tests\test_audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
