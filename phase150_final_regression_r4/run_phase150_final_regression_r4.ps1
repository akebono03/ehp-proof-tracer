$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Final Regression R4"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Purpose: Phase 150 final full regression"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogPath = Join-Path $RepoRoot "phase150_final_regression_r4_output.txt"
$TracePath = Join-Path $RepoRoot "phase150_final_regression_r4_trace.log"

$env:PYTHONPATH = "$ScriptRoot;$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"
$env:PHASE150_TRACE_LOG = $TracePath

try {
    if (Test-Path $LogPath) {
        Remove-Item $LogPath -Force
    }
    if (Test-Path $TracePath) {
        Remove-Item $TracePath -Force
    }

    Write-Host ""
    Write-Host "A. Collect-only preflight..."
    python -m pytest tests --collect-only -q 2>&1 |
      Tee-Object -FilePath $LogPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Collect-only preflight failed."
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Final full regression..."
    Write-Host "Detailed START/END tracing begins at 30%."
    Write-Host "Trace log: $TracePath"
    Write-Host "Pytest output: $LogPath"
    $Started = Get-Date

    python -m pytest `
      tests `
      -q `
      --tb=line `
      --durations=50 `
      --durations-min=1.0 `
      -p phase150_final_regression_r4_trace_plugin `
      2>&1 |
      Tee-Object -FilePath $LogPath -Append

    $ExitCode = $LASTEXITCODE
    $Elapsed = ((Get-Date) - $Started).TotalSeconds

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Full regression elapsed: $([math]::Round($Elapsed, 2))s"
    Write-Host "Full regression exit code: $ExitCode"
    Write-Host "Pytest output: $LogPath"
    Write-Host "Trace log: $TracePath"
    Write-Host "=============================================================="

    if ($ExitCode -eq 0) {
        Write-Host "PHASE 150 FINAL REGRESSION: PASS"
    }
    else {
        Write-Host "PHASE 150 FINAL REGRESSION: FAIL"
    }

    exit $ExitCode
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
    Remove-Item Env:PHASE150_TRACE_LOG -ErrorAction SilentlyContinue
}
