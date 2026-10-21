$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Join-Path $root 'phase167_r4_remove_obsolete_renderer'
$previous = $env:PYTHONPATH
$env:PYTHONPATH = "$root;$previous"
$results = Join-Path $root 'phase167_r4_remove_obsolete_renderer_results'
$before = Join-Path $results 'before'
$after = Join-Path $results 'after'
$backup = Join-Path $results 'backups'
New-Item -ItemType Directory -Force -Path $before,$after,$backup | Out-Null
$files = @('phase165_r56_presentation_adapter.py','phase165_r57_r10_step_narrative.py')
$changed = $false
try {
    python "$package\capture.py" $before
    if ($LASTEXITCODE -ne 0) { throw 'Baseline capture failed; nothing changed' }
    foreach ($file in $files) { Copy-Item -LiteralPath (Join-Path $root $file) -Destination (Join-Path $backup $file) -Force }
    $changed = $true
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { throw 'Install failed' }
    python -c "from phase165_r56_presentation_adapter import render_completed_shared_narrative; from phase165_r57_r10_step_narrative import ordered_proof_ancestry,has_transport_proof_ancestry; import phase165_r57_r10_step_narrative as m; assert not hasattr(m,'render_completed_from_proofsteps')"
    if ($LASTEXITCODE -ne 0) { throw 'Import and deletion check failed' }
    python "$package\capture.py" $after
    if ($LASTEXITCODE -ne 0) { throw 'After capture failed' }
    python "$package\compare.py" $before $after
    if ($LASTEXITCODE -ne 0) { throw 'Narrative/search regression' }
    python -m pytest -q phase165_r57_r10_proofstep_fidelity/test_phase165_r57_r10_proofstep_fidelity.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    Write-Host 'PASS: old renderer removed, 1-stem baselines intact; full pytest NOT run.'
} catch {
    if ($changed) { foreach ($file in $files) { Copy-Item -LiteralPath (Join-Path $backup $file) -Destination (Join-Path $root $file) -Force } }
    Write-Host 'ROLLBACK: original production files restored.'
    throw
} finally {
    $env:PYTHONPATH = $previous
}
