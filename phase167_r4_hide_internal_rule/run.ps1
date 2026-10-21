$ErrorActionPreference='Stop'
$root=(Get-Location).Path
$pkg=Join-Path $root 'phase167_r4_hide_internal_rule'
$prev=$env:PYTHONPATH
$env:PYTHONPATH="$root;$prev"
$results=Join-Path $root 'phase167_r4_hide_internal_rule_results'
$before=Join-Path $results 'before'
$after=Join-Path $results 'after'
$backup=Join-Path $results 'backup'
New-Item -ItemType Directory -Force -Path $before,$after,$backup | Out-Null
$file='toda_group_proof_narrative_shared_components.py'
$changed=$false
try {
  python "$pkg\capture.py" $before
  if($LASTEXITCODE -ne 0){throw 'Baseline capture failed'}
  Copy-Item -LiteralPath (Join-Path $root $file) -Destination (Join-Path $backup $file) -Force
  $changed=$true
  python "$pkg\install.py"
  if($LASTEXITCODE -ne 0){throw 'Install failed'}
  python "$pkg\capture.py" $after
  if($LASTEXITCODE -ne 0){throw 'After capture failed'}
  python "$pkg\compare.py" $before $after
  if($LASTEXITCODE -ne 0){throw 'Full narrative comparison failed'}
  python -m pytest -q --import-mode=importlib "$pkg\test_hide_rule.py"
  if($LASTEXITCODE -ne 0){throw 'Targeted pytest failed'}
  Write-Host 'PASS: R4 item 1 only. Full pytest NOT run.'
} catch {
  if($changed){Copy-Item -LiteralPath (Join-Path $backup $file) -Destination (Join-Path $root $file) -Force; Write-Host 'ROLLBACK: restored original shared components'}
  throw
} finally { $env:PYTHONPATH=$prev }
