$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 150 Performance Diagnostic R3"
Write-Host "32% per-test stall locator"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="
$RepoRoot=(Get-Location).Path
$ScriptRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH="$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING="utf-8"
try {
 python "$ScriptRoot\diagnose_phase150_performance_r3.py" --percent 32 --before 20 --after 20 --timeout 60
 $ExitCode=$LASTEXITCODE
 Write-Host ""
 Write-Host "=============================================================="
 Write-Host "Diagnostic exit code: $ExitCode"
 Write-Host "Upload:"
 Write-Host "  .\phase150_performance_diagnostic_r3_output\REPORT.txt"
 Write-Host "  .\phase150_performance_diagnostic_r3_output\timing_detail.txt"
 Write-Host "=============================================================="
 exit $ExitCode
} finally {
 Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
 Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
