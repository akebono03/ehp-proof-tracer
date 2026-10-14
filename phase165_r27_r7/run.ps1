$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_app.py')) { throw 'Run from ehp-proof-tracer repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B (Join-Path $bundle 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Legacy dependency audit failed' }
python -m pytest -q (Join-Path $bundle 'test_r27_r7_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R7 targeted pytest failed' }
Write-Output 'R27-R7 read-only audit completed; full pytest NOT run.'
