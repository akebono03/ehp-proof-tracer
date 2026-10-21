$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase167_r4_typed_rule_suppression'
$oldPythonPath = $env:PYTHONPATH
$target = Join-Path $root 'toda_group_proof_narrative_renderer.py'
$backup = Join-Path $folder 'renderer_before.py.bak'
$modified = $false
try {
  $env:PYTHONPATH = $root
  python "$folder\capture.py"
  if ($LASTEXITCODE -ne 0) { throw 'Before capture failed' }
  Copy-Item "$folder\capture.json" "$folder\before.json" -Force
  python "$folder\install.py"
  if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
  $modified = $true
  python "$folder\capture.py"
  if ($LASTEXITCODE -ne 0) { throw 'After capture failed' }
  Copy-Item "$folder\capture.json" "$folder\after.json" -Force
  python "$folder\check.py"
  if ($LASTEXITCODE -ne 0) { throw 'Golden narrative comparison failed' }
  python -m pytest -q --import-mode=importlib "$folder\test_typed_display.py"
  if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
  Write-Host 'PASS: Phase 167 R4-1. Full pytest NOT run.'
} catch {
  if ($modified -and (Test-Path $backup)) {
    Copy-Item $backup $target -Force
    Write-Host 'ROLLBACK: original renderer restored'
  }
  throw
} finally {
  $env:PYTHONPATH = $oldPythonPath
}
