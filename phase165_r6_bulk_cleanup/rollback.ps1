param([Parameter(Mandatory=$true)][string]$Session)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
python (Join-Path $PSScriptRoot 'rollback.py') $root $Session
if ($LASTEXITCODE -ne 0) { throw 'Rollback failed.' }
