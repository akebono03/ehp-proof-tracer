$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_36e_search_context_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "R3-36E runtime audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\\test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-36E limited tests failed" }
    Write-Host "R3-36E read-only audit complete. Full suite NOT run."
}
finally {
    Pop-Location
}
