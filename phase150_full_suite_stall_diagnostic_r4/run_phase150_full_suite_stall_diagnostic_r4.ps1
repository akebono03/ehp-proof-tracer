$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 150 Full-Suite Stall Diagnostic R4"
Write-Host "Single-process full-suite trace from 30%"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "=============================================================="
$RepoRoot=(Get-Location).Path
$ScriptRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$Trace=Join-Path $RepoRoot "phase150_full_suite_stall_diagnostic_r4_trace.txt"
$Console=Join-Path $RepoRoot "phase150_full_suite_stall_diagnostic_r4_console.txt"
$env:PYTHONPATH="$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING="utf-8"
try {
 Remove-Item $Trace -ErrorAction SilentlyContinue
 Remove-Item $Console -ErrorAction SilentlyContinue
 Write-Host ""
 Write-Host "A. Running the real full suite in ONE pytest process..."
 Write-Host "Trace is flushed from 30% to:"
 Write-Host "  $Trace"
 Write-Host ""
 Write-Host "If the console stalls, open another PowerShell and run:"
 Write-Host "  Get-Content .\phase150_full_suite_stall_diagnostic_r4_trace.txt -Tail 20"
 Write-Host ""
 python -m pytest tests -q -p "$ScriptRoot\phase150_stall_trace_plugin.py" 2>&1 | Tee-Object -FilePath $Console
 $ExitCode=$LASTEXITCODE
 Write-Host ""
 Write-Host "=============================================================="
 Write-Host "Diagnostic pytest exit code: $ExitCode"
 Write-Host "Trace:   .\phase150_full_suite_stall_diagnostic_r4_trace.txt"
 Write-Host "Console: .\phase150_full_suite_stall_diagnostic_r4_console.txt"
 Write-Host "Full completion is NOT required for this diagnostic."
 Write-Host "=============================================================="
 exit $ExitCode
} finally {
 Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
 Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
