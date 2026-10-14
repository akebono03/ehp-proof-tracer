$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $dir
Push-Location $root
try {
    python "$dir\apply.py"
    if ($LASTEXITCODE -ne 0) { throw 'R57 audit failed' }
    python -m pytest -q "$dir\test_installer.py"
    if ($LASTEXITCODE -ne 0) { throw 'R57 targeted tests failed' }
    Write-Host 'R27-R57 retirement gate and targeted tests passed; full pytest NOT run.'
} finally {
    Pop-Location
}
