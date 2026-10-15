$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$package;$root"
python -m pytest -q (Join-Path $package 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R16 audit tests failed.' }
python (Join-Path $package 'audit.py') $root
if ($LASTEXITCODE -ne 0) { throw 'R5-R16 prerequisites failed. No application changes were performed.' }
Write-Host 'R5-R16 retirement audit recorded. No application files modified; full pytest NOT run.'
