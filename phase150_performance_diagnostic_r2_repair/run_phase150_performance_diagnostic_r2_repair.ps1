$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Performance Diagnostic R2 Repair"
Write-Host "Builder recomputation timing"
Write-Host "Repair: add repository tests directory to Python import path"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    python "$ScriptRoot\diagnose_phase150_performance_r2_repair.py"
    $ExitCode = $LASTEXITCODE
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Diagnostic exit code: $ExitCode"
Write-Host "Upload:"
Write-Host "  .\phase150_performance_diagnostic_r2_output\REPORT.txt"
Write-Host "  .\phase150_performance_diagnostic_r2_output\timing_detail.txt"
Write-Host "=============================================================="

exit $ExitCode
