$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
