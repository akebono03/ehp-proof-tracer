$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
python '.\phase165_r27_r17\apply.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R17 installation failed' }
python -m pytest -q '.\phase165_r27_r17\test_phase165_r27_r17.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R17 targeted pytest failed' }
Write-Host 'R27-R17 targeted checks passed; full pytest NOT run.'
