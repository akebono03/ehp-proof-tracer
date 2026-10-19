$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $PSScriptRoot
python -m pytest -q test_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R6-12 targeted test failed' }
Set-Location $repo
python ".\phase165_r6_12_probe_dependency\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R6-12 audit failed' }
Write-Host 'R6-12 read-only audit completed; full pytest NOT run.'
