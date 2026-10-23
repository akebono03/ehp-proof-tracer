$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$repo;$env:PYTHONPATH"
python "$package\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'Frozen audit failed' }
Write-Host 'Audit only; no repository files modified; full pytest NOT run.'
