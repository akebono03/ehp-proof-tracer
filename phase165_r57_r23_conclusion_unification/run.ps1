$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo
$source = Join-Path $PSScriptRoot 'phase165_r57_r23_conclusion_unification.py'
$target = Join-Path $repo 'phase165_r57_r23_conclusion_unification.py'
Copy-Item -LiteralPath $source -Destination $target -Force
Write-Output 'R23 shared conclusion unification installed (new module only).'
python -m pytest -q (Join-Path $PSScriptRoot 'test_phase165_r57_r23_conclusion_unification.py')
if ($LASTEXITCODE -ne 0) { throw 'R23 targeted pytest FAILED' }
Write-Output 'R23 targeted pytest PASSED; full pytest NOT run.'
