$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3y_actual_context.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-Y audit failed' }
    Write-Host 'R3-Y read-only audit finished; full pytest NOT run.'
} finally { Pop-Location }
