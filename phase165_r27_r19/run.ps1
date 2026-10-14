$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $here 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R19 installation failed' }
python -m pytest -q (Join-Path $here 'test_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R19 targeted pytest failed' }
Write-Host 'R27-R19 targeted checks passed; full pytest NOT run.'
