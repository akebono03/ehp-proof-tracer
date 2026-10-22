$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $folder
Push-Location $repo
try {
    python -m pytest -q "$folder\tests\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'Audit tests failed' }
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'Audit execution failed' }
} finally {
    Pop-Location
}
