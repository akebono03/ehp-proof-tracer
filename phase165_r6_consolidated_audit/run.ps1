$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw "Consolidated audit failed: $LASTEXITCODE" }
Write-Host 'READ-ONLY TRIAGE COMPLETE; no tests or production files altered; full pytest NOT run.'
