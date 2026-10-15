$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $project 'phase165_r52_r9_shared_math.py'))) { throw 'Run from EHP project root.' }
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R26 install FAILED' }
python -m pytest -q (Join-Path $package 'test_phase165_r57_r26_generic_search_connection.py') (Join-Path $package 'test_phase165_r57_r26_integration.py')
if ($LASTEXITCODE -ne 0) { throw 'R26 targeted pytest FAILED' }
Write-Host 'R26 targeted pytest PASSED; full pytest NOT run.'
