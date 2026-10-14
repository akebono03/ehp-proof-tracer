$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_app.py')) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Install failed' }
$env:PYTHONPATH = (Get-Location).Path
python -B -m pytest -q (Join-Path $bundle 'test_phase165_r27_r6_legacy_entry_cut.py') '.\test_phase165_r52_r5_auto_search.py' '.\test_phase165_r52_r4_flask_connection.py'
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Host 'R27-R6 targeted tests passed; full pytest NOT run.'
