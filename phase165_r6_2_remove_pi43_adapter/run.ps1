$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = $PSScriptRoot
if (-not (Test-Path (Join-Path $root 'phase165_r52_r9_shared_math.py'))) { throw 'Run at the repository root.' }
python -m pytest -q (Join-Path $package 'test_apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Pre-install tests failed; nothing changed.' }
python (Join-Path $package 'apply.py') --root $root
if ($LASTEXITCODE -ne 0) { throw 'Removal failed.' }
python -c "import phase165_r52_r9_shared_math; from phase165_r52_r9_shared_math import shared_expansion_provider; print('Shared provider import: PASS')"
if ($LASTEXITCODE -ne 0) { throw 'Production import check failed. Restore the backed-up shared file and adapter.' }
Write-Host 'Targeted tests complete. Full pytest NOT run.'
