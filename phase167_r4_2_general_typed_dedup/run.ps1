$ErrorActionPreference='Stop'
$here=Split-Path -Parent $MyInvocation.MyCommand.Path
$root=Split-Path -Parent $here
Set-Location $root
$target=Join-Path $root 'toda_group_proof_narrative_argument_body_renderer.py'
$backup=Join-Path $root 'phase167_r4_2_general_typed_dedup_backup\original_argument_body_renderer.py'
python "$here\capture.py" before.json
if ($LASTEXITCODE -ne 0) { throw 'Before capture failed' }
try {
  python "$here\install.py"
  if ($LASTEXITCODE -ne 0) { throw 'Install failed' }
  python "$here\capture.py" after.json
  if ($LASTEXITCODE -ne 0) { throw 'After capture failed' }
  python "$here\check.py"
  if ($LASTEXITCODE -ne 0) { throw 'Narrative regression failed' }
  python -m pytest -q "$here\test_typed_display.py"
  if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
  Write-Host 'PASS: Phase 167 R4-2; full pytest NOT run'
} catch {
  if (Test-Path $backup) { Copy-Item $backup $target -Force; Write-Host 'ROLLBACK: restored prior renderer' }
  throw
}
