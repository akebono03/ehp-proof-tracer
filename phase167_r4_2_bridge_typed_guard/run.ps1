$ErrorActionPreference = 'Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONPATH=$root + [IO.Path]::PathSeparator + $env:PYTHONPATH
$target=Join-Path $root 'toda_group_proof_narrative_contribution_renderer.py'
$backup=Join-Path $PSScriptRoot 'original_renderer_backup.py'
if (Test-Path $backup) { throw 'Backup already exists; remove prior extracted package directory before retrying' }
python (Join-Path $PSScriptRoot 'capture.py') before
if ($LASTEXITCODE -ne 0) { throw 'Before capture failed; renderer unchanged' }
Copy-Item $target $backup
try {
  python (Join-Path $PSScriptRoot 'install.py')
  if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
  python (Join-Path $PSScriptRoot 'capture.py') after
  if ($LASTEXITCODE -ne 0) { throw 'After capture failed' }
  python (Join-Path $PSScriptRoot 'check.py')
  if ($LASTEXITCODE -ne 0) { throw 'Narrative comparison failed' }
  python -m pytest -q (Join-Path $PSScriptRoot 'test_typed_bridge.py')
  if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
  Write-Host 'PASS: Phase 167 R4-2. Full pytest NOT run.'
} catch {
  Copy-Item $backup $target -Force
  Write-Host 'ROLLBACK: previous renderer restored'
  throw
}
