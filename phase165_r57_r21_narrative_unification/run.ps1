$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python was not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21 install failed' }
& $python -m pytest -q (Join-Path $package 'test_phase165_r57_r21_narrative_unification.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21 targeted pytest failed' }
Write-Output 'R57-R21 targeted tests passed; full pytest NOT run.'
