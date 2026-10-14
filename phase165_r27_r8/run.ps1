$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\main.py')) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
python -m pytest -q (Join-Path $bundle 'test_phase165_r27_r8.py')
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Host 'R27-R8 targeted tests passed; full pytest NOT run.'
