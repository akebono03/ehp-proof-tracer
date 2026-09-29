$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Test Performance Repair 5"
Write-Host "Phase144-6 R5-42 shared production/context reuse"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Target = "tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py"

Write-Host "`nA. Applying R5-42 shared context/production fixtures..."
python "$PackageDir\apply_test_performance_repair_5.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nB. Syntax preflight..."
python -m py_compile $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Running R5-42 with durations..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
python -m pytest -q $Target --durations=20
$pytestExit = $LASTEXITCODE
$sw.Stop()
Write-Host ("R5-42 wall clock: {0:N2}s" -f $sw.Elapsed.TotalSeconds)
if ($pytestExit -ne 0) { exit $pytestExit }

Write-Host "`nD. Diff verification..."
git diff --check -- $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git diff --numstat -- $Target
git diff -- $Target

Write-Host "`n=============================================================="
Write-Host "Repair 5 focused completion criteria:"
Write-Host "  - 9 passed"
Write-Host "  - production changes: none"
Write-Host "  - audit builder changes: none"
Write-Host "  - six target contexts created once per module"
Write-Host "  - production rows derived from those same contexts"
Write-Host "  - Phase40 and Phase41 independent audit comparisons retained"
Write-Host "  - determinism still rebuilds production on the same context"
Write-Host "  - substantial runtime reduction from repeated context rebuilds"
Write-Host "No full suite is run in this performance repair."
Write-Host "=============================================================="
