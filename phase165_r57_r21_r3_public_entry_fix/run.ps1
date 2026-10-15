$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21-R3 apply/runtime verification failed' }
& $python -m pytest -q (Join-Path $package 'test_phase165_r57_r21_r3_public_entry_fix.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21-R3 targeted pytest failed' }
$prior = Join-Path $project 'phase165_r57_r21_narrative_unification'
& $python -m pytest -q (Join-Path $prior 'test_phase165_r57_r21_narrative_unification.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21 original six tests still fail' }
Write-Output 'R57-R21-R3 targeted tests passed; full pytest NOT run.'
