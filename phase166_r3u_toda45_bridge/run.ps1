$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python ".\phase166_r3u_toda45_bridge\apply.py"
    if ($LASTEXITCODE -ne 0) { throw "R3-U patch failed" }
    python -m pytest -q ".\phase166_r3u_toda45_bridge\test_r3u.py" ".\phase165_r57_r7_toda45_backward_connection\test_phase165_r57_r7_toda45_backward_connection.py"
    if ($LASTEXITCODE -ne 0) { throw "R3-U targeted tests failed. Restore the original from backups." }
    Write-Host "R3-U targeted PASS; full pytest NOT run."
} finally {
    Pop-Location
}
