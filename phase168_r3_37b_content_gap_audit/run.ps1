$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_37b_content_gap_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited tests failed" }
    Write-Host "R3-37B read-only audit completed. Full suite NOT run."
}
finally {
    Pop-Location
}
