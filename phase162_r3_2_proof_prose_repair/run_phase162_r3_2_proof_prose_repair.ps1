$ErrorActionPreference = "Stop"
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $bundle
Push-Location $repo
try {
    python -B (Join-Path $bundle "apply_phase162_r3_2_proof_prose_repair.py")
    if ($LASTEXITCODE -ne 0) { throw "Prose repair apply failed" }
    python -B -m pytest -q `
        "tests/test_phase162_r3_narrative_connection.py" `
        (Join-Path $bundle "tests/test_phase162_r3_prose_regression.py") `
        (Join-Path $bundle "tests/test_phase162_r3_2_verified_group_connection.py") `
        "tests/test_phase162_r2_existing_proof_connection.py"
    if ($LASTEXITCODE -ne 0) { throw "Prose repair focused tests failed" }
    Write-Output "Phase 162 R3 prose repair focused tests passed. Full suite not run."
} finally {
    Pop-Location
}
