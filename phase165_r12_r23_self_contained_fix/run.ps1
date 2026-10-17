$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$env:PYTHONPATH = $project + [IO.Path]::PathSeparator + $env:PYTHONPATH
$package = Join-Path $project 'phase165_r12_r23_self_contained_fix'
if (-not (Test-Path (Join-Path $package 'phase165_r12_r23_public_narrative.py'))) { throw 'Run from project root' }
Copy-Item (Join-Path $package 'phase165_r12_r23_public_narrative.py') (Join-Path $project 'phase165_r12_r23_public_narrative.py') -Force
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r23_public_narrative.py') (Join-Path $package 'tests/test_phase165_r12_r23_path_fix.py') (Join-Path $package 'tests/test_phase165_r12_r23_runner_fix.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R23 focused pytest failed' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R23 audit failed' }
Write-Host 'R12-R23 audit complete; full pytest NOT run. Inspect public_narrative.md for wording and citation quality.'
