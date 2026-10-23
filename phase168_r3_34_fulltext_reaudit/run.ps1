$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $package
try {
    python -m pytest -q ".\tests\test_fulltext_reaudit.py"
    if ($LASTEXITCODE -ne 0) { throw "Focused tests failed" }
    python ".\audit.py"
    if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
    Write-Host "R3-34 AUDIT_ONLY: source files unchanged; full pytest NOT run."
} finally { Pop-Location }
