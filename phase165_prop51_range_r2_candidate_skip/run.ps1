$ErrorActionPreference = 'Stop'
$root = (Resolve-Path '.').Path
$package = Join-Path $root 'phase165_prop51_range_r2_candidate_skip'
python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Install failed' }
python -m pytest -q (Join-Path $package 'test_candidate_skip.py')
if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
Write-Output 'Prop51 candidate rejection now returns no candidates; full pytest NOT run.'
