$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ClosurePackage = Join-Path `
  $RepoRoot `
  "phase155_closure"
$ClosureRunner = Join-Path `
  $ClosurePackage `
  "run_phase155_closure.ps1"
$ClosurePlugin = Join-Path `
  $ClosurePackage `
  "phase155_closure_progress_plugin.py"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure R1 - progress plugin repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Cause:"
Write-Host "  pytest TestReport has no .config attribute."
Write-Host ""
Write-Host "Repair:"
Write-Host "  replace only the Closure progress plugin;"
Write-Host "  use direct flushed output instead of report.config/terminalreporter."
Write-Host ""
Write-Host "IMPORTANT: after the lightweight preflight passes,"
Write-Host "the phase-final repository-wide pytest will run again."
Write-Host "This is HEAVY."
Write-Host "The previous failed run executed only 1 of 10421 tests."
Write-Host ""

if (-not (Test-Path $ClosureRunner)) {
  throw "Required Phase 155 Closure package not found: $ClosureRunner"
}

Write-Host "1/3 Lightweight repaired-plugin self-tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_progress_plugin.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure progress-plugin self-tests failed."
}

Write-Host ""
Write-Host "2/3 Replace only the Closure progress plugin"

Copy-Item `
  "$PackageDir\phase155_closure_progress_plugin.py" `
  $ClosurePlugin `
  -Force

Write-Host "replaced: $ClosurePlugin"
Write-Host "production changes: none"
Write-Host "existing repository-test changes: none"

Write-Host ""
Write-Host "3/3 Resume Phase 155 Closure"
Write-Host "The full suite starts from the beginning because the previous"
Write-Host "pytest process terminated after test 1/10421."
Write-Host "No meaningful completed full-suite work is being discarded."
Write-Host ""

powershell -ExecutionPolicy Bypass `
  -File $ClosureRunner

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155 Closure still failed after progress-plugin repair."
}

Write-Host ""
Write-Host "Phase 155 Closure R1 completed."
