$ErrorActionPreference = "Stop"
$project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $project
try {
    python -m phase168_r3_38_frozen_fulltext_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "R3-38 audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-38 limited tests failed" }
    Write-Host "R3-38 read-only audit complete. Full suite NOT run."
}
finally {
    Pop-Location
}
