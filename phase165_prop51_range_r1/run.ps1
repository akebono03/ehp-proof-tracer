$ErrorActionPreference = 'Stop'
$root = (Resolve-Path '.').Path
$package = Join-Path $root 'phase165_prop51_range_r1'
Copy-Item (Join-Path $package 'phase165_prop51_range_guard.py') (Join-Path $root 'phase165_prop51_range_guard.py') -Force
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Install failed' }
python -m pytest -q (Join-Path $package 'test_range.py')
if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
Write-Output 'Prop51 range update installed; full pytest NOT run.'
