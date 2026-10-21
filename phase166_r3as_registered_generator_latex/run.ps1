$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python .\phase166_r3as_registered_generator_latex\apply.py
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    python -m pytest -q .\phase166_r3as_registered_generator_latex\test_r3as.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    Write-Host 'Targeted pytest PASS; full pytest NOT run.'
} finally {
    Pop-Location
}
