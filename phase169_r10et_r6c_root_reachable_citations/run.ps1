param()
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$scriptPath = Join-Path $PSScriptRoot 'run.py'
python $scriptPath --repo (Get-Location).Path
$code = $LASTEXITCODE
Write-Host "R10ET_R6C_EXIT=$code"
exit $code
