$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Old = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $PSScriptRoot
    python -m pytest -q (Join-Path $PSScriptRoot 'test_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    python (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
} finally {
    $env:PYTHONPATH = $Old
}
Write-Host 'R6-1 R3 read-only triage complete; full pytest NOT run.'
