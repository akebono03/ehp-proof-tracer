$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
Write-Host 'Phase 164 R8-R7 factory residual closure'
$env:PYTHONPATH = "$PSScriptRoot;$project;$env:PYTHONPATH"
python -B -m pytest -q -p no:cacheprovider "$PSScriptRoot\tests\test_r8_r7_patch.py"
if ($LASTEXITCODE -ne 0) { throw 'R8-R7 package tests failed; no source changed' }
python -B "$PSScriptRoot\apply.py" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R8-R7 preflight failed; no source changed' }
python -B "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R8-R7 apply failed; check audit and backup' }
python -B -m pytest -q -p no:cacheprovider `
  "$PSScriptRoot\tests\test_r8_r7_patch.py" `
  tests/test_proof.py `
  tests/test_phase164_r8_r2_factory_contract.py `
  tests/test_phase161_r5_backward_proof_reconstruction.py `
  tests/test_phase161_r7_premise_provenance_validation.py `
  tests/test_phase110_10_operation_query_proof_replay.py
if ($LASTEXITCODE -ne 0) {
  Write-Warning 'R8-R7 focused tests failed; rolling back'
  python -B "$PSScriptRoot\rollback.py"
  if ($LASTEXITCODE -ne 0) { throw 'Rollback failed; recover from the R8-R7 backup folder' }
  throw 'R8-R7 tests failed; source changes reverted'
}
Write-Host 'R8-R7 targeted pytest PASS; full pytest NOT run.'
