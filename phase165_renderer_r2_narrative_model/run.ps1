$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { $project } else { "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R2 install failed' }
& $python -m pytest -q (Join-Path $package 'test_phase165_renderer_r2_narrative_model.py')
if ($LASTEXITCODE -ne 0) { throw 'R2 targeted pytest failed' }
Write-Output 'R2 model installed. Targeted pytest passed; existing renderers unchanged; full pytest NOT run.'
