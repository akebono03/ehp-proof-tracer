$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_36d_screened_bridge_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "R3-36D audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-36D limited tests failed" }
    Write-Host "R3-36D completed. Full suite NOT run."
}
finally {
    Pop-Location
}
