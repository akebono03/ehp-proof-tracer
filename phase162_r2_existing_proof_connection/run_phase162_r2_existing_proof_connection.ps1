$ErrorActionPreference = "Stop"
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $bundle
if (!(Test-Path (Join-Path $repo "proof.py")) -or !(Test-Path (Join-Path $repo "toda_rules.py"))) {
    throw "Run this bundle inside the EHP Proof Tracer repository root."
}
Copy-Item (Join-Path $bundle "phase162_group_structure_backward.py") (Join-Path $repo "phase162_group_structure_backward.py") -Force
Copy-Item (Join-Path $bundle "phase162_r2_existing_proof_connection.py") (Join-Path $repo "phase162_r2_existing_proof_connection.py") -Force
Copy-Item (Join-Path $bundle "tests\test_phase162_r2_existing_proof_connection.py") (Join-Path $repo "tests\test_phase162_r2_existing_proof_connection.py") -Force
Push-Location $repo
try {
    python -B -m pytest -q tests/test_phase162_group_structure_backward.py tests/test_phase162_r2_existing_proof_connection.py tests/test_phase161_r5_backward_proof_reconstruction.py tests/test_phase161_r6_proof_reconstruction_audit.py
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed ($LASTEXITCODE)." }
    Write-Output "Phase 162 R2 focused tests passed. Full suite not run."
} finally {
    Pop-Location
}
