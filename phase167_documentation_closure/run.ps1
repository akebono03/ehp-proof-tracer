$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$script = Join-Path $PSScriptRoot 'update_docs.py'
python $script
if ($LASTEXITCODE -ne 0) { throw 'Phase167 documentation closure failed' }
