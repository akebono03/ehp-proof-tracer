$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_36b_runtime_link_audit_importfix.audit
    if ($LASTEXITCODE -ne 0) { throw "Runtime audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    Write-Host "R3-36B runtime linkage inspection completed. Full suite NOT run."
}
finally {
    Pop-Location
}
