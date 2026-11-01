param()
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Output 'PHASE173_R3_FRONTIER_FOCUSED_PYTEST_START'
python -B -m pytest -q -p no:cacheprovider '.\phase173_r3_frontier_readout\tests\test_readout.py'
if ($LASTEXITCODE -ne 0) { throw 'R3 frontier focused pytest failed' }
Write-Output 'PHASE173_R3_FRONTIER_FOCUSED_PYTEST=PASS'
python -B -m phase173_r3_frontier_readout.readout
if ($LASTEXITCODE -ne 0) { throw 'R3 frontier readout failed' }
git status -sb
