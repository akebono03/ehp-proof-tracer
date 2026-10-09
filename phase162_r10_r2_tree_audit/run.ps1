$ErrorActionPreference = 'Stop'
$Repo = (Get-Location).Path
$Package = Join-Path $Repo 'phase162_r10_r2_tree_audit'
if (-not (Test-Path (Join-Path $Repo 'phase162_pi5_3_web_replay.py'))) {
    throw 'Run this script from the EHP Proof Tracer repository root.'
}
if (-not (Test-Path (Join-Path $Repo 'phase162_reference_boundary.py'))) {
    throw 'R10 citation boundary implementation was not found. Apply R10 first.'
}
Write-Host 'Phase 162 R10-R2 read-only proof-tree audit'
python -B -m phase162_r10_r2_tree_audit.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest phase162_r10_r2_tree_audit/tests/test_audit.py -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Read-only audit finished. Full pytest not run.'
