$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_37_public_narrative_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "Narrative audit failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\\test_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited test failed" }
    Write-Host "R3-37 audit completed. No full pytest."
}
finally {
    Pop-Location
}
