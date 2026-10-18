$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python -m phase165_reference_stop_r1.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q '.\phase165_reference_stop_r1\test_audit.py'
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
