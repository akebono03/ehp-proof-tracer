$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Apply failed' }
python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_phase166_r3_order_only.py') 'phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py' 'tests/test_phase165_r3_recursive_search.py'
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Output 'Targeted tests complete. Full pytest NOT run.'
