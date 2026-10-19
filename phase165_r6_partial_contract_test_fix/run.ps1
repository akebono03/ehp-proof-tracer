$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python -X utf8 (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw "Phase 165 partial-contract targeted tests failed: $LASTEXITCODE" }
