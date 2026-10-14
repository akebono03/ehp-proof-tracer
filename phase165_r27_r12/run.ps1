$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_app.py')) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B (Join-Path $bundle 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R12 audit failed' }
python -B -m pytest -q (Join-Path $bundle 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R12 targeted pytest failed' }
Write-Host 'R27-R12 read-only audit completed; full pytest NOT run.'
