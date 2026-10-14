$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R52-R12 installation failed' }
python -m pytest -q test_phase165_typed_component_lookup.py test_phase165_r52_r12_component_bridge.py test_phase165_r52_r9_shared_math.py
if ($LASTEXITCODE -ne 0) { throw 'R52-R12 targeted pytest failed' }
Write-Host 'R52-R12 targeted tests passed; full pytest NOT run.'
