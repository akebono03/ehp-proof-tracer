$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python ".\phase165_r27_r16\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R27-R16 installation failed' }
python -m pytest -q ".\phase165_r27_r16\test_phase165_r27_r16.py"
if ($LASTEXITCODE -ne 0) { throw 'R27-R16 targeted pytest failed' }
Write-Host 'R27-R16 targeted checks passed; full pytest NOT run.'
