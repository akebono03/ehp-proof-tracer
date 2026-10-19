param([Parameter(Mandatory = $true)][string]$SessionDirectory)
$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
python (Join-Path $PSScriptRoot 'rollback.py') $project $SessionDirectory
if ($LASTEXITCODE -ne 0) { throw "Rollback failed: $LASTEXITCODE" }
