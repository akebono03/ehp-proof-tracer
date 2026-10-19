param([Parameter(Mandatory=$true)][string]$Report)
$ErrorActionPreference = 'Stop'
python "$PSScriptRoot\rollback.py" "$Report" --root (Get-Location).Path
if ($LASTEXITCODE -ne 0) { throw 'Rollback stopped due to safety check' }
