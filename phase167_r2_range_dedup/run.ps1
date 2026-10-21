$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    $env:PYTHONPATH = $repo
    python ".\phase167_r2_range_dedup\apply.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Copy-Item ".\phase167_r2_range_dedup\test_phase167_r2_range_dedup.py" ".\tests\test_phase167_r2_range_dedup.py" -Force
    python -m pytest -q tests/test_phase167_r2_range_dedup.py tests/test_phase167_r2_unified_reference.py tests/test_phase167_r2_shared_reference.py tests/test_phase144_6_r3_structured_references.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
