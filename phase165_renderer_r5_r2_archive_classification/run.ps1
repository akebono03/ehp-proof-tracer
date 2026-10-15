$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { "$project$([IO.Path]::PathSeparator)$package" } else { "$project$([IO.Path]::PathSeparator)$package$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) {
    Write-Output 'R5 R2: active legacy imports remain. The report lists their exact paths. Application source unchanged.'
    throw 'R5 R2 static audit failed; inspect audit_output\review.md'
}
& $python -m pytest -q (Join-Path $package 'test_r5.py') (Join-Path $project 'test_phase165_r56_common_renderer.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 R2 targeted tests failed; no application source changed.' }
Write-Output 'R5 R2 active-route static audit passed; inspect helper candidates before declaring complete. Full pytest NOT run.'
