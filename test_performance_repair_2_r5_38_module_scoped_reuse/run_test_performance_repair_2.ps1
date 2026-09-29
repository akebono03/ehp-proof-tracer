$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Test Performance Repair 2"
Write-Host "Phase144-6 R5-38 module-scoped audit data reuse"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Target = "tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py"

Write-Host "`nA. Applying test-only module-scoped fixture reuse..."
python "$PackageDir\apply_test_performance_repair_2.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nB. Syntax preflight..."
python -m py_compile $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Running R5-38 with durations..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
python -m pytest -q $Target --durations=20
$pytestExit = $LASTEXITCODE
$sw.Stop()
Write-Host ("R5-38 wall clock: {0:N2}s" -f $sw.Elapsed.TotalSeconds)
if ($pytestExit -ne 0) { exit $pytestExit }

Write-Host "`nD. Diff verification..."
git diff --check -- $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git diff --numstat -- $Target
git diff -- $Target

Write-Host "`n=============================================================="
Write-Host "Repair 2 focused completion criteria:"
Write-Host "  - 6 passed"
Write-Host "  - production changes: none"
Write-Host "  - audit builder changes: none"
Write-Host "  - R5-38 expensive datasets each created once per module"
Write-Host "  - substantial runtime reduction from repeated per-test rebuilds"
Write-Host "No full suite is run in this performance repair."
Write-Host "=============================================================="
