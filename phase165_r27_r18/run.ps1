$ErrorActionPreference = 'Stop'
python '.\phase165_r27_r18\apply.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R18 install failed' }
python -m pytest -q '.\phase165_r27_r18\test_patch.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R18 targeted pytest failed' }
Write-Host 'R27-R18 targeted checks passed; full pytest NOT run.'
