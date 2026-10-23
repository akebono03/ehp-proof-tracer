$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
    python -m phase168_r3_37c_toda45_tabfix.apply
    if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
    python -m pytest -q `
      (Join-Path $PSScriptRoot "tests\test_tex_arrow.py") `
      (Join-Path $root "phase168_r3_37c_typed_projection\tests\test_reference_projection.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    Write-Host "R3-37C LaTeX arrow corrected. Full suite NOT run."
}
finally { Pop-Location }
