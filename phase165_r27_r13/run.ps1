$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_app.py')) { throw 'Execute from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B (Join-Path $bundle 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R13 audit failed' }
$env:PYTHONPATH = "$bundle;$((Get-Location).Path)"
python -B -m pytest -q (Join-Path $bundle 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R13 targeted pytest failed' }
Write-Host 'R27-R13 read-only classification completed; full pytest NOT run.'
