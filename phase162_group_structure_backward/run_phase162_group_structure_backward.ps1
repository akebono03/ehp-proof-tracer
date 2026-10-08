$ErrorActionPreference = 'Stop'
$bundle = $PSScriptRoot
$root = (Get-Location).Path
if (!(Test-Path (Join-Path $root 'proof.py')) -or !(Test-Path (Join-Path $root 'phase161_r5_backward_proof_reconstruction.py'))) {
    throw 'Run from the EHP Proof Tracer repository root.'
}
$testDir = Join-Path $root 'tests'
if (!(Test-Path $testDir)) { throw 'Missing tests directory.' }
Copy-Item -LiteralPath (Join-Path $bundle 'phase162_group_structure_backward.py') -Destination (Join-Path $root 'phase162_group_structure_backward.py') -Force
Copy-Item -LiteralPath (Join-Path $bundle 'tests\test_phase162_group_structure_backward.py') -Destination (Join-Path $testDir 'test_phase162_group_structure_backward.py') -Force
python -B -m pytest -q tests/test_phase162_group_structure_backward.py tests/test_phase161_r5_backward_proof_reconstruction.py tests/test_phase161_r6_proof_reconstruction_audit.py
if ($LASTEXITCODE -ne 0) { throw "Focused tests failed ($LASTEXITCODE)" }
Write-Host 'Focused tests passed. Full suite not run.'
