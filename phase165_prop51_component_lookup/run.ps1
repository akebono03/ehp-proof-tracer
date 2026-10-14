$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -LiteralPath (Join-Path $package 'phase165_typed_component_lookup.py') -Destination $root -Force
Copy-Item -LiteralPath (Join-Path $package 'test_phase165_typed_component_lookup.py') -Destination $root -Force
python -m pytest -q test_phase165_typed_component_lookup.py
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Host 'Read-only typed component lookup installed. Full pytest NOT run.'
