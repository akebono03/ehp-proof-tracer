$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Set-Location $Package
python -m pytest -q -p no:cacheprovider '.\test_audit.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python '.\audit.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R6-1 classification completed (read-only). Full pytest NOT run.'
