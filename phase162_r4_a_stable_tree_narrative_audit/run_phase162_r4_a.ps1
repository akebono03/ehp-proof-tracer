$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase162_r4_a_stable_tree_narrative_audit'
if (-not (Test-Path (Join-Path $repo 'toda_group_proof_narrative_renderer.py'))) {
    throw 'Run this script from the EHP Proof Tracer repository root.'
}
if (-not (Test-Path (Join-Path $package 'phase162_r4_a_audit.py'))) {
    throw 'Audit package not found. Expand the ZIP into the repository root.'
}
python -B -m pytest 'phase162_r4_a_stable_tree_narrative_audit/tests/test_phase162_r4_a_audit.py' -q
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed; audit not run.' }
python -B -m phase162_r4_a_stable_tree_narrative_audit.phase162_r4_a_audit
if ($LASTEXITCODE -ne 0) { throw 'Audit execution failed.' }
Write-Host 'Phase 162 R4-A focused checks completed; full suite not run.'
