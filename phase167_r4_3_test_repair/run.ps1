$ErrorActionPreference = "Stop"
$TestFile = Join-Path $PSScriptRoot "test_phase167_r4_3_homomorphism_theorem.py"
python -m pytest $TestFile -q
if ($LASTEXITCODE -ne 0) {
    throw "Phase 167 R4-3 limited pytest FAILED (exit $LASTEXITCODE)"
}
Write-Host "Phase 167 R4-3 limited pytest PASSED"
Write-Host "Production code unchanged. Full pytest not run."
