$ErrorActionPreference = 'Stop'
$project=(Get-Location).Path
if (-not (Test-Path (Join-Path $project 'phase165_r55_nk_only_goal.py'))) { throw 'Run from project root.' }
$env:PYTHONPATH="$project;$env:PYTHONPATH"
$dir=Join-Path $project 'phase165_r2_display_results'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$base=Join-Path $dir 'pi3_2_before.md'
$target=Join-Path $project 'toda_group_proof_narrative_renderer.py'
$original=Join-Path $project 'phase165_r2_renderer_before.py.bak'
if (Test-Path $original) { throw 'Existing R2 backup found; do not overwrite.' }
python -c "from pathlib import Path; from phase165_r55_nk_only_goal import search_group_from_registered_goal; from phase165_r52_partial_proof import render_partial_proof_markdown; r=search_group_from_registered_goal(n=2,k=1); assert r.status.value=='complete'; Path('phase165_r2_display_results/pi3_2_before.md').write_text(render_partial_proof_markdown(r),encoding='utf-8')"
if ($LASTEXITCODE -ne 0) { throw 'Baseline generation failed; nothing changed.' }
python "$PSScriptRoot\patch.py"
if ($LASTEXITCODE -ne 0) { throw 'Patch failed.' }
python "$PSScriptRoot\check.py"
if ($LASTEXITCODE -ne 0) {
  Copy-Item -LiteralPath $original -Destination $target -Force
  Write-Host 'R2 checks failed; original renderer restored.'
  throw 'R2 regression test failed.'
}
Write-Host 'R2 targeted checks passed. Full pytest NOT run.'
