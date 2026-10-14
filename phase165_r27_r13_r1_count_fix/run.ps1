$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\web_app.py')) { throw 'Execute from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python -B (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R13-R1 install failed' }
python -B '.\phase165_r27_r13\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R27-R13 audit failed' }
$env:PYTHONPATH = "$(Join-Path (Get-Location).Path 'phase165_r27_r13');$bundle;$((Get-Location).Path)"
python -B -m pytest -q '.\phase165_r27_r13\test_audit.py' (Join-Path $bundle 'test_count_fix.py')
if ($LASTEXITCODE -ne 0) { throw 'R27-R13-R1 targeted pytest failed' }
Write-Host 'R27-R13-R1 classification and regression tests passed; full pytest NOT run.'
