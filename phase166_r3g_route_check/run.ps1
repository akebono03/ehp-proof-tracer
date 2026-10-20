$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo
$env:PYTHONPATH = $repo
python (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-G route audit failed' }
Write-Host 'R3-G read-only check complete; full pytest NOT run.'
