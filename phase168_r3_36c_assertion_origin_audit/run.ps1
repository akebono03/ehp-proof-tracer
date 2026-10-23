$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_36c_assertion_origin_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "R3-36C audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\\test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-36C limited tests failed" }
    Write-Host "R3-36C completed. Full suite NOT run."
}
finally {
    Pop-Location
}
