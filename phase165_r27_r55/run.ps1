$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python '.\phase165_r27_r55\apply.py'
    if ($LASTEXITCODE -ne 0) { throw 'R55 installation failed' }
    python -m pytest -q '.\phase165_r27_r55\test_installer.py'
    if ($LASTEXITCODE -ne 0) { throw 'R55 targeted tests failed' }
    Write-Host 'R27-R55 targeted tests passed; full pytest NOT run.'
} finally { Pop-Location }
