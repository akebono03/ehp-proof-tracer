$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Repository root: $repo"
$required = @('proof.py', 'phase161_r5_backward_proof_reconstruction.py', 'tests/test_phase161_r6_proof_reconstruction_audit.py')
foreach ($file in $required) {
    if (-not (Test-Path (Join-Path $repo $file))) { throw "Missing prerequisite: $file" }
}
Copy-Item (Join-Path $package 'phase161_r7_premise_provenance_validation.py') (Join-Path $repo 'phase161_r7_premise_provenance_validation.py') -Force
Copy-Item (Join-Path $package 'tests/test_phase161_r7_premise_provenance_validation.py') (Join-Path $repo 'tests/test_phase161_r7_premise_provenance_validation.py') -Force
python -B -m pytest -q tests/test_phase161_r7_premise_provenance_validation.py tests/test_phase161_r6_proof_reconstruction_audit.py
if ($LASTEXITCODE -ne 0) { throw "R7 focused tests failed with exit code $LASTEXITCODE" }
Write-Host 'R7 focused tests passed; entire suite NOT run.'
