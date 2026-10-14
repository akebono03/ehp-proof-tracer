$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python '.\phase165_r27_r54\apply.py'
    if ($LASTEXITCODE -ne 0) { throw 'R54 dependency audit failed' }
    python -m pytest -q '.\phase165_r27_r54\test_installer.py'
    if ($LASTEXITCODE -ne 0) { throw 'R54 targeted tests failed' }
    Write-Host 'R27-R54 dependency audit and targeted tests passed; full pytest NOT run.'
} finally { Pop-Location }
