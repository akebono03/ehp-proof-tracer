$ErrorActionPreference = 'Stop'
if (-not (Test-Path (Join-Path (Get-Location).Path 'web_app.py'))) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B (Join-Path $bundle 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Audit failed: missing required source file' }
python -B -m pytest -q (Join-Path $bundle 'test_phase165_r27_r9_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Output 'R27-R9 read-only audit completed; full pytest NOT run.'
