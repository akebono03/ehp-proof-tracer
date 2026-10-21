$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    $source = Join-Path $PSScriptRoot "test_phase167_r2_shared_reference.py"
    $destination = Join-Path $repo "tests\test_phase167_r2_shared_reference.py"
    Copy-Item -Path $source -Destination $destination -Force
    python -m pytest -q tests/test_phase167_r2_shared_reference.py tests/test_phase144_6_r3_structured_references.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
