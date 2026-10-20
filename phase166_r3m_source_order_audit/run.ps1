$ErrorActionPreference = 'Stop'
$Repo = (Get-Location).Path
$Bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Repo
python (Join-Path $Bundle 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-M audit failed' }
Write-Host 'R3-M read-only audit finished; no production changes and no pytest.'
