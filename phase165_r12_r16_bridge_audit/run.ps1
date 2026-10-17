$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -LiteralPath (Join-Path $package 'phase165_r12_r16_bridges.py') -Destination (Join-Path $root 'phase165_r12_r16_bridges.py') -Force
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $package 'tests/test_phase165_r12_r16_bridges.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R16 focused pytest failed' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R16 audit failed; see audit_result.json' }
Write-Host 'R12-R16 bridge audit finished. Full pytest NOT run.'
