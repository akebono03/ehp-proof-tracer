$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$script = Join-Path $PSScriptRoot 'audit.py'
python $script --repo $repo --output (Join-Path $PSScriptRoot 'results')
if ($LASTEXITCODE -ne 0) { throw 'R2 audit failed' }
python -m pytest -q (Join-Path $PSScriptRoot 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R2 focused tests failed' }
Write-Host 'R2 generator/group audit PASS; production unchanged; full pytest NOT run.'
