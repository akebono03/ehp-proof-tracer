$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_37c_toda45_iso_fix.apply
    if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
    python -m pytest -q `
      (Join-Path $PSScriptRoot "tests\test_toda45_iso.py") `
      (Join-Path $root "phase168_r3_37c_typed_projection\tests\test_reference_projection.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited tests failed" }
    Write-Host "R3-37C iso fix completed. Full suite NOT run."
}
finally {
    Pop-Location
}
