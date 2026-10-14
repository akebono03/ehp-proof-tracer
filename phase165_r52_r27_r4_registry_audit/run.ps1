$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
python -m pytest -q (Join-Path $PSScriptRoot 'test_audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R4 registry audit complete; production unchanged; full pytest NOT run.'
