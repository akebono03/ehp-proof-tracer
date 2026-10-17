$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python -m phase165_r12_r34_r4_scope_gate.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest -q ".\phase165_r12_r34_r4_scope_gate\test_audit.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
