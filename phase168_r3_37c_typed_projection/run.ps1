$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    Copy-Item (Join-Path $PSScriptRoot "phase168_r3_37c_reference_projection.py") (Join-Path $root "phase168_r3_37c_reference_projection.py") -Force
    python -m phase168_r3_37c_typed_projection.apply
    if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\test_reference_projection.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    Write-Host "R3-37C: limited tests completed. Full suite NOT run."
}
finally { Pop-Location }
