$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Test Performance Repair 9"
Write-Host "Phase144-6 R5-43-11c family inventory reuse"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

$Targets = @(
  "tests\test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py",
  "tests\test_phase144_6_r5_43_11c_r2_argument_participation_guard.py"
)

Write-Host "`nA. Applying R5-43-11c family module-scoped fixtures..."
python "$PackageDir\apply_test_performance_repair_9.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nB. Syntax preflight..."
python -m py_compile $Targets
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Running R5-43-11c family with durations..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
python -m pytest -q $Targets --durations=20
$pytestExit = $LASTEXITCODE
$sw.Stop()
Write-Host ("R5-43-11c family wall clock: {0:N2}s" -f $sw.Elapsed.TotalSeconds)
if ($pytestExit -ne 0) { exit $pytestExit }

Write-Host "`nD. Diff verification..."
git diff --check -- $Targets
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git diff --numstat -- $Targets
git diff -- $Targets

Write-Host "`n=============================================================="
Write-Host "Repair 9 focused completion criteria:"
Write-Host "  - 6 passed"
Write-Host "  - production changes: none"
Write-Host "  - audit builder changes: none"
Write-Host "  - each module builds six target contexts once"
Write-Host "  - each module builds its inventory once"
Write-Host "  - 11c definition-group test reuses shared contexts"
Write-Host "  - existing assertions remain intact"
Write-Host "No full suite is run in this performance repair."
Write-Host "=============================================================="
