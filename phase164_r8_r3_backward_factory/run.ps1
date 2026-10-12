$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
$env:PYTHONPATH = (Get-Location).Path
python (Join-Path $PSScriptRoot 'apply_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R8-R3 patch failed' }
New-Item -ItemType Directory -Path '.\tests' -Force | Out-Null
Copy-Item -Path (Join-Path $PSScriptRoot 'tests\test_phase164_r8_r3_backward_factory.py') -Destination '.\tests\test_phase164_r8_r3_backward_factory.py' -Force
python -m pytest -q tests/test_phase164_r8_r3_backward_factory.py tests/test_phase164_r8_r2_factory_contract.py tests/test_phase161_r5_backward_proof_reconstruction.py tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw 'R8-R3 targeted pytest failed' }
Write-Host 'Phase 164 R8-R3 backward proof factory connected; full pytest NOT run.'
