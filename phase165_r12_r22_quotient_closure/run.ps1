$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item (Join-Path $package 'phase165_r12_r22_quotient_closure.py') (Join-Path $root 'phase165_r12_r22_quotient_closure.py') -Force
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r22_quotient_closure.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R22 focused tests failed' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R22 proof audit remains unresolved' }
Write-Host 'R12-R22 quotient closure certified; full pytest NOT run.'
