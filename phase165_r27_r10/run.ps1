$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_group_proof.py')) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R10 install failed' }
python -m pytest -q (Join-Path $bundle 'test_phase165_r27_r10.py') 'test_phase165_r52_r4_flask_connection.py' 'test_phase165_r52_r5_auto_search.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R10 targeted pytest failed' }
Write-Host 'R27-R10 targeted checks passed; full pytest NOT run.'
