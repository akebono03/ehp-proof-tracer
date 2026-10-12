$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
$env:PYTHONPATH = (Get-Location).Path
Copy-Item -Path (Join-Path $PSScriptRoot 'phase164_r8_proofstep_factory.py') -Destination '.\phase164_r8_proofstep_factory.py' -Force
Copy-Item -Path (Join-Path $PSScriptRoot 'tests\test_phase164_r8_r2_factory_contract.py') -Destination '.\tests\test_phase164_r8_r2_factory_contract.py' -Force
Write-Host 'R8-R2 additive factory installed; proof.py and existing callers unchanged.'
python -m pytest -q tests/test_phase164_r8_r2_factory_contract.py tests/test_phase161_r5_backward_proof_reconstruction.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R8-R2 focused tests failed' }
Write-Host 'Phase 164 R8-R2 focused tests PASS; full pytest NOT run.'
