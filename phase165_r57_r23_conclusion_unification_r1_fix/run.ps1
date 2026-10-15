$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'phase165_r57_r23_conclusion_unification.py') -Destination (Join-Path $repo 'phase165_r57_r23_conclusion_unification.py') -Force
Write-Output 'R23-R1 unification fix installed.'
python -m pytest -q (Join-Path $PSScriptRoot 'test_phase165_r57_r23_conclusion_unification.py')
if ($LASTEXITCODE -ne 0) { throw 'R23-R1 targeted pytest FAILED' }
Write-Output 'R23-R1 targeted pytest PASSED; full pytest NOT run.'
