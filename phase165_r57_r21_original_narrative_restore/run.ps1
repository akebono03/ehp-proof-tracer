$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Narrative restore install FAILED' }
& $python -m pytest -q (Join-Path $package 'test_original_narrative_restore.py')
if ($LASTEXITCODE -ne 0) { throw 'Narrative restore targeted pytest FAILED' }
Write-Output 'Original Narrative route restored; targeted pytest PASSED; full pytest NOT run.'
