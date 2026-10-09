$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo
python -B (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 163 R1 inventory finished. Source code unchanged; full pytest suite not run.'
