$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3g_route_check_path_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-G route audit failed' }
    Write-Host 'R3-G route audit completed; production code unchanged; full pytest NOT run.'
}
finally {
    Pop-Location
}
