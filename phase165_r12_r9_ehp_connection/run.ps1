$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = 'utf-8'
python -m pytest -q .\phase165_r12_r9_ehp_connection\tests\test_phase165_r12_r9_ehp_connection.py
if ($LASTEXITCODE -ne 0) { throw 'R12-R9 targeted pytest failed' }
python -m phase165_r12_r9_ehp_connection.audit
if ($LASTEXITCODE -ne 0) { throw 'R12-R9 audit failed' }
Write-Host 'R12-R9 read-only audit complete. Full pytest NOT run.'
