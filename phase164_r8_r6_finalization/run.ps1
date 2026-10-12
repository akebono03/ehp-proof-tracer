$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
Write-Host 'Phase 164 R8-R6 guarded residual ProofStep routing'
$env:PYTHONPATH = "$PSScriptRoot;$project;$env:PYTHONPATH"
python -B -m pytest -q -p no:cacheprovider "$PSScriptRoot\tests\test_r8_r6_patch.py"
if ($LASTEXITCODE -ne 0) { throw 'R8-R6 package tests failed; nothing changed' }
python -B "$PSScriptRoot\apply.py" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R8-R6 precheck failed; nothing changed' }
python -B "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R8-R6 migration failed; inspect backup' }
python -B -m pytest -q -p no:cacheprovider `
  "$PSScriptRoot\tests\test_r8_r6_factory.py" `
  tests/test_phase164_r8_r2_factory_contract.py `
  tests/test_phase161_r5_backward_proof_reconstruction.py `
  tests/test_phase161_r7_premise_provenance_validation.py `
  tests/test_phase110_10_operation_query_proof_replay.py
if ($LASTEXITCODE -ne 0) {
  Write-Warning 'Focused tests failed; reverting R8-R6 changes'
  python -B "$PSScriptRoot\rollback.py"
  if ($LASTEXITCODE -ne 0) { throw 'R8-R6 tests and rollback failed; restore from backup' }
  throw 'R8-R6 focused tests failed; reverted R8-R6 changes'
}
Write-Host 'R8-R6 focused tests PASS; full pytest NOT run. See phase164_r8_r6_output\audit.json.'
