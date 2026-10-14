$ErrorActionPreference = 'Stop'
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R11 installation failed' }
python -m pytest -q (Join-Path $bundle 'test_phase165_r27_r11.py') test_phase165_r52_r4_flask_connection.py test_phase165_r52_r5_auto_search.py
if ($LASTEXITCODE -ne 0) { throw 'R27-R11 targeted pytest failed' }
Write-Output 'R27-R11 targeted checks passed; full pytest NOT run.'
