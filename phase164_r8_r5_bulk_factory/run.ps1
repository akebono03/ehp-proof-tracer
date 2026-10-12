$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
Write-Host 'Phase 164 R8-R5 guarded batch migration'
python -B -m pytest -q -p no:cacheprovider "$PSScriptRoot\tests\test_bulk_migration.py"
if ($LASTEXITCODE -ne 0) { throw 'R8-R5 migration guard tests failed; no files changed' }
python -B "$PSScriptRoot\apply.py" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R8-R5 precheck failed; no files changed' }
python -B "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R8-R5 migration failed; inspect backup/output' }
python -B -m pytest -q -p no:cacheprovider `
  tests/test_phase164_r8_r2_factory_contract.py `
  tests/test_phase161_r5_backward_proof_reconstruction.py `
  tests/test_phase161_r7_premise_provenance_validation.py `
  tests/test_phase110_10_operation_query_proof_replay.py
if ($LASTEXITCODE -ne 0) {
  Write-Warning 'Focused pytest failed; restoring R8-R5 modified files.'
  python -B "$PSScriptRoot\rollback.py"
  if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed and rollback failed; restore from R8-R5 backup directory' }
  throw 'R8-R5 focused tests failed; automatic rollback completed'
}
Write-Host 'R8-R5 batch migration PASS. Full pytest NOT run. Legacy GIVEN evidence remains unverified unless already verified.'
Write-Host 'Output: phase164_r8_r5_output\audit.json and CHANGED_CODE.md'
