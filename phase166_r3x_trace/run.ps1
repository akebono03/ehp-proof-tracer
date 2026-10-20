$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3x_trace.trace
    if ($LASTEXITCODE -ne 0) { throw 'R3-X trace failed' }
    Write-Host 'R3-X read-only trace finished; full pytest NOT run.'
} finally { Pop-Location }
