$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { $package } else { "$package$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python -m pytest -q (Join-Path $package 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R1 targeted audit tests failed; no project files were modified' }
& $python (Join-Path $package 'audit.py') --project $project --output (Join-Path $package 'audit_output')
if ($LASTEXITCODE -ne 0) { throw 'R1 read-only inventory failed' }
Write-Output 'R1 read-only Renderer audit completed; no application code changed; full pytest NOT run.'
