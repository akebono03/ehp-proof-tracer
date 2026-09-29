$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Test Performance Repair 6"
Write-Host "Phase144-6 R5-43-4 _pi6_data() module-scoped reuse"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Target = "tests\test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py"

Write-Host "`nA. Applying R5-43-4 module-scoped pi6_data fixture..."
python "$PackageDir\apply_test_performance_repair_6.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nB. Syntax preflight..."
python -m py_compile $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Running R5-43-4 with durations..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
python -m pytest -q $Target --durations=20
$pytestExit = $LASTEXITCODE
$sw.Stop()
Write-Host ("R5-43-4 wall clock: {0:N2}s" -f $sw.Elapsed.TotalSeconds)
if ($pytestExit -ne 0) { exit $pytestExit }

Write-Host "`nD. Diff verification..."
git diff --check -- $Target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git diff --numstat -- $Target
git diff -- $Target

Write-Host "`n=============================================================="
Write-Host "Repair 6 focused completion criteria:"
Write-Host "  - 6 passed"
Write-Host "  - production changes: none"
Write-Host "  - audit builder changes: none"
Write-Host "  - _pi6_data() created once per module"
Write-Host "  - five behavioral tests reuse the same pi6 data"
Write-Host "  - existing assertions remain unchanged"
Write-Host "  - substantial runtime reduction from repeated pi6 reconstruction"
Write-Host "No full suite is run in this performance repair."
Write-Host "=============================================================="
