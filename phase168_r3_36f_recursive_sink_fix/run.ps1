$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_36f_recursive_sink_fix.apply
    if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
    python -m pytest -q (Join-Path $PSScriptRoot "tests\test_context_handoff.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    Write-Host "R3-36F recursive sink fix complete. Full suite NOT run."
}
finally { Pop-Location }
