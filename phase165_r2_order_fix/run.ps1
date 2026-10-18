$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path '.\phase165_r55_nk_only_goal.py')) { throw 'Run from project root.' }
if (-not (Test-Path '.\phase165_r2_renderer_before.py.bak')) { throw 'Previous R2 patch backup missing; refuse unknown baseline.' }
$env:PYTHONPATH = "$root;$env:PYTHONPATH"
$results = Join-Path $root 'phase165_r2_order_fix_results'
New-Item -ItemType Directory -Path $results -Force | Out-Null
$before = Join-Path $results 'pi3_2_before.md'
$target = Join-Path $root 'toda_group_proof_narrative_renderer.py'
$backup = Join-Path $root 'phase165_r2_order_fix_before.py.bak'
if (Test-Path $backup) { throw 'Order repair backup exists; refusing second install.' }
python -c "from pathlib import Path; from phase165_r55_nk_only_goal import search_group_from_registered_goal; from phase165_r52_partial_proof import render_partial_proof_markdown; r=search_group_from_registered_goal(n=2,k=1); assert r.status.value=='complete'; Path('phase165_r2_order_fix_results/pi3_2_before.md').write_text(render_partial_proof_markdown(r),encoding='utf-8')"
if ($LASTEXITCODE -ne 0) { throw 'Pre-patch pi3_2 baseline failed. No changes made.' }
python "$PSScriptRoot\patch.py"
if ($LASTEXITCODE -ne 0) { throw 'Patch failed.' }
python "$PSScriptRoot\check.py"
if ($LASTEXITCODE -ne 0) {
  if (Test-Path $backup) {
    Copy-Item -LiteralPath $backup -Destination $target -Force
    Write-Host 'Checks failed: original file restored.'
  }
  throw 'Order regression failure'
}
Write-Host 'Targeted regression PASS. Full pytest NOT run.'
