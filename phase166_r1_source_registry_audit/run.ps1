$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
    $env:PYTHONPATH = "$folder;$root"
    python -m pytest -q "$folder\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
    Write-Host 'R1 source-registry read-only audit finished; full pytest NOT run.'
} finally {
    Pop-Location
}
