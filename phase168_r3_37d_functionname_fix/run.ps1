$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_37d_functionname_fix.apply
    if ($LASTEXITCODE -ne 0) { throw "R3-37D patch failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\test_general_reference.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    Write-Host "R3-37D function-name fix complete. Full suite NOT run."
}
finally {
    Pop-Location
}
