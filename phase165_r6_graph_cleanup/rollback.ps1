param([Parameter(Mandatory=$true)][string]$Session)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$folder\rollback.py" --root (Get-Location).Path --session $Session
if ($LASTEXITCODE -ne 0) { throw 'Rollback failed' }
