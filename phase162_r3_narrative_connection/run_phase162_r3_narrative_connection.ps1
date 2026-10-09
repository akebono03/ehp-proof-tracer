$ErrorActionPreference = "Stop"
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $bundle
if (!(Test-Path (Join-Path $repo "proof.py")) -or !(Test-Path (Join-Path $repo "phase162_r2_existing_proof_connection.py"))) {
    throw "Run this bundle inside the EHP Proof Tracer repository root after Phase 162 R2."
}
Copy-Item (Join-Path $bundle "phase162_r3_narrative_connection.py") (Join-Path $repo "phase162_r3_narrative_connection.py") -Force
Copy-Item (Join-Path $bundle "tests\test_phase162_r3_narrative_connection.py") (Join-Path $repo "tests\test_phase162_r3_narrative_connection.py") -Force
Push-Location $repo
try {
    python -B -m pytest -q tests/test_phase162_r3_narrative_connection.py tests/test_phase162_r2_existing_proof_connection.py tests/test_phase162_group_structure_backward.py
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed ($LASTEXITCODE)." }
    Write-Output "Phase 162 R3 focused tests passed. Full suite not run."
} finally {
    Pop-Location
}
