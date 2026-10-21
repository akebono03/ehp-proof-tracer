$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3ar_exceptional_notation.apply
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    python -m pytest -q .\phase166_r3ar_exceptional_notation\tests\test_r3ar_exceptional_notation.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    Write-Host 'Targeted tests PASS; full pytest NOT run.'
} finally { Pop-Location }
