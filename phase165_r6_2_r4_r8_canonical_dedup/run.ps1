$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase165_r6_2_r4_r8_canonical_dedup'
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $folder 'test_install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installer tests failed; no production change' }
python (Join-Path $folder 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installer failed' }
python -m pytest -q (Join-Path $folder 'test_integration.py') (Join-Path $root 'tests/test_phase165_r3_recursive_search.py')
if ($LASTEXITCODE -ne 0) { throw 'Targeted regression failed' }
Write-Output 'R4-R8 installed; targeted pytest passed; full pytest NOT run.'
