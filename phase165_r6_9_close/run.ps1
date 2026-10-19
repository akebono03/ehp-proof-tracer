$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'close.py')
if ($LASTEXITCODE -ne 0) { throw "R6-9 failed: see report.json" }
Write-Host 'R6-9 targeted collection completed; full pytest NOT run.'
