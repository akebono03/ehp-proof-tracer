$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python (Join-Path $PSScriptRoot 'diagnose.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Diagnostic complete; read-only, full pytest NOT run.'
