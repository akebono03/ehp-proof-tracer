$ErrorActionPreference = "Stop"
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $bundle
$focusedTest = Join-Path $bundle "tests\test_phase162_r3_2_verified_group_connection.py"
if (!(Test-Path $focusedTest)) {
    throw "R3-2 focused test file was not found in the extracted ZIP folder: $focusedTest"
}
Push-Location $repo
try {
    python -B (Join-Path $bundle "apply_phase162_r3_2.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-2 apply failed" }
    python -B -m pytest -q `
        $focusedTest `
        "tests/test_phase162_r3_narrative_connection.py" `
        "tests/test_phase162_r2_existing_proof_connection.py"
    if ($LASTEXITCODE -ne 0) { throw "R3-2 focused tests failed" }
    Write-Output "R3-2 focused tests passed. Full suite not run."
} finally {
    Pop-Location
}
