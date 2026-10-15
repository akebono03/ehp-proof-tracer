$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21-R1 install/verification failed' }
& $python -m pytest -q (Join-Path $package 'test_phase165_r57_r21_r1_effective_renderer_fix.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21-R1 targeted pytest failed' }
& $python -m pytest -q (Join-Path $project 'phase165_r57_r21_narrative_unification' 'test_phase165_r57_r21_narrative_unification.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21 regression pytest failed' }
Write-Output 'R57-R21-R1 targeted tests passed; full pytest NOT run.'
