$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python (Join-Path $PSScriptRoot 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Phase 166 R3-Z install failed' }
python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_phase166_r3z_publication_order_unification.py')
if ($LASTEXITCODE -ne 0) { throw 'Phase 166 R3-Z targeted tests failed' }
Write-Host 'Targeted tests completed; full pytest not run.'
