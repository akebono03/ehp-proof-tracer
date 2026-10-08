$ErrorActionPreference = "Stop"
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $bundle
Push-Location $repo
try {
    python -B (Join-Path $bundle "apply_phase162_r3_2_repair3.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-2 repair3 apply failed" }
    python -B -m pytest -q `
        (Join-Path $bundle "tests\test_phase162_r3_2_verified_group_connection.py") `
        "tests/test_phase162_r2_existing_proof_connection.py" `
        "tests/test_phase162_r3_narrative_connection.py"
    if ($LASTEXITCODE -ne 0) { throw "R3-2 repair3 focused tests failed" }
    Write-Output "R3-2 repair3 focused tests passed. Full suite not run."
} finally {
    Pop-Location
}
