$ErrorActionPreference = 'Stop'
$RepoRoot = (Get-Location).Path
$PackageDir = $PSScriptRoot
if (!(Test-Path (Join-Path $RepoRoot 'phase161_r7_premise_provenance_validation.py'))) {
    throw 'Run from the ehp-proof-tracer repository root after Phase 161 R7.'
}
Copy-Item (Join-Path $PackageDir 'files\phase162_validated_proof_presentation.py') (Join-Path $RepoRoot 'phase162_validated_proof_presentation.py') -Force
Copy-Item (Join-Path $PackageDir 'files\tests\test_phase162_r2_validated_proof_presentation.py') (Join-Path $RepoRoot 'tests\test_phase162_r2_validated_proof_presentation.py') -Force
python -B -m pytest -q tests/test_phase162_r2_validated_proof_presentation.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 162 R2 focused tests completed. Full test suite not run.'
