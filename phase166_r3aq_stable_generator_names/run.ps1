$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3aq_stable_generator_names.apply
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    python -m pytest -q .\phase166_r3aq_stable_generator_names\test_r3aq.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
    Write-Host 'Targeted tests PASS; full pytest NOT run.'
} finally {
    Pop-Location
}
