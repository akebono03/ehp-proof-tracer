$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R21 installation failed' }
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r21_eta_generator_chain.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R21 tests failed' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R21 audit unresolved' }
Write-Host 'R12-R21 focused checks completed; full pytest NOT run.'
