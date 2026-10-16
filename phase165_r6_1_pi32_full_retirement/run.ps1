$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Removal not applied' }
python -m pytest -q (Join-Path $PSScriptRoot 'test_retirement.py')
if ($LASTEXITCODE -ne 0) { throw 'Focused regression failed' }
Write-Host 'R6-1 obsolete pi32 search removed; full pytest NOT run.'
