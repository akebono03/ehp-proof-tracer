$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q (Join-Path $PSScriptRoot 'test_patch.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R23 targeted tests passed; full pytest NOT run.'
