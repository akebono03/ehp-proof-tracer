$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R24 installation failed' }
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r24_web_search_connection.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R24 focused pytest failed' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R24 Web search audit failed' }
Write-Host 'R12-R24 Web canonical search audit recorded. Full pytest NOT run.'
