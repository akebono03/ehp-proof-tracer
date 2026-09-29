$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Test Performance Repair 7"
Write-Host "Phase144-6 R5-43-7 hidden-bridge inventory / semantic reuse"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Target = "tests\test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py"

Write-Host "`nA. Applying R5-43-7 module-scoped fixtures..."
python "$PackageDir\apply_test_performance_repair_7.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nB. Syntax preflight..."
python -m py_compile $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Running R5-43-7 with durations..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
python -m pytest -q $Target --durations=20
$pytestExit = $LASTEXITCODE
$sw.Stop()
Write-Host ("R5-43-7 wall clock: {0:N2}s" -f $sw.Elapsed.TotalSeconds)
if ($pytestExit -ne 0) { exit $pytestExit }

Write-Host "`nD. Diff verification..."
git diff --check -- $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git diff --numstat -- $Target
git diff -- $Target

Write-Host "`n=============================================================="
Write-Host "Repair 7 focused completion criteria:"
Write-Host "  - 5 passed"
Write-Host "  - production changes: none"
Write-Host "  - audit builder changes: none"
Write-Host "  - hidden-bridge inventory created once per module"
Write-Host "  - semantic-by-signature map created once per module"
Write-Host "  - determinism test still invokes semantic builder twice"
Write-Host "  - existing assertions remain intact"
Write-Host "No full suite is run in this performance repair."
Write-Host "=============================================================="
