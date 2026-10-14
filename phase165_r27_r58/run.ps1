$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
Push-Location $root
try {
    python "$here\apply.py"
    if ($LASTEXITCODE -ne 0) { throw 'R58 installation failed' }
    python -m pytest -q "$here\test_installer.py"
    if ($LASTEXITCODE -ne 0) { throw 'R58 targeted tests failed' }
    Write-Host 'R27-R58 CLI Group route migration targeted tests passed; full pytest NOT run.'
} finally {
    Pop-Location
}
