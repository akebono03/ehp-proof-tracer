$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Join-Path $root 'phase165_r6_2_r4_r4_stage5'
$env:PYTHONPATH = "$root;$package"
python -m pytest -q (Join-Path $package 'test_install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installer unit tests failed' }
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
python -m pytest -q (Join-Path $package 'test_integration.py') (Join-Path $root 'tests/test_map_property_rules.py') (Join-Path $root 'tests/test_phase165_r8_rule_provider.py')
if ($LASTEXITCODE -ne 0) { throw 'Targeted integration/regression tests failed' }
Write-Output 'R4-4 stage5 installed; targeted tests PASS; full pytest NOT run.'
