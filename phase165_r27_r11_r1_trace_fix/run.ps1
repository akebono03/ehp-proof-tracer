$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_group_proof_common.py')) { throw 'Run from repository root after R27-R10' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R11-R1 installation failed' }
python -m pytest -q `
  (Join-Path $bundle 'test_phase165_r27_r11_r1_trace_fix.py') `
  '.\phase165_r27_r11\test_phase165_r27_r11.py' `
  'test_phase165_r52_r4_flask_connection.py' `
  'test_phase165_r52_r5_auto_search.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R11-R1 targeted pytest failed' }
Write-Output 'R27-R11-R1 targeted checks passed; full pytest NOT run.'
