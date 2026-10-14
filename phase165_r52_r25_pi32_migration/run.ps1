$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $package
try {
    python -m pytest -q test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R25 targeted pytest failed' }
    python audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R25 audit failed' }
    Write-Host 'R25 compatibility gate completed; production unchanged; full pytest NOT run.'
} finally { Pop-Location }
