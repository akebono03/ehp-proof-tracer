$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { "$project$([IO.Path]::PathSeparator)$package" } else { "$project$([IO.Path]::PathSeparator)$package$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 static audit failed. Review audit_output\review.md; no source was changed.' }
& $python -m pytest -q (Join-Path $package 'test_r5.py') (Join-Path $project 'test_phase165_r56_common_renderer.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 targeted tests failed. Source was not changed.' }
Write-Output 'R5 structural and runtime audit passed; review helper ownership candidates; full pytest NOT run.'
