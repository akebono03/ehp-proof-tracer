$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Final Regression R3"
Write-Host "Final full regression after Performance Repair R1/R2"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Output = Join-Path $RepoRoot "phase150_final_regression_r3.txt"
$Summary = Join-Path $RepoRoot "phase150_final_regression_r3_summary.txt"

$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Final full pytest regression with duration reporting..."
    Write-Host "   This is the only full-suite run for Final Regression R3."
    Write-Host ""

    $Started = Get-Date

    python -m pytest tests -q `
      --durations=50 `
      --durations-min=1.0 `
      2>&1 |
      Tee-Object -FilePath $Output

    $PytestExit = $LASTEXITCODE
    $Elapsed = (Get-Date) - $Started

    $Status = if ($PytestExit -eq 0) { "PASS" } else { "FAIL" }
    $NextAction = if ($PytestExit -eq 0) {
        "Phase 150 documentation/closure. Do NOT rerun the full suite."
    } else {
        "Inspect only the reported failures. Do NOT rerun the full suite yet."
    }

    $SummaryLines = @(
        "Phase 150 Final Regression R3",
        "==============================================================",
        "Regression status: $Status",
        "pytest exit code: $PytestExit",
        ("Elapsed seconds: {0:N2}" -f $Elapsed.TotalSeconds),
        "Full output: $Output",
        "Next action: $NextAction"
    )

    $SummaryLines | Set-Content -Path $Summary -Encoding UTF8

    Write-Host ""
    Write-Host "=============================================================="
    foreach ($Line in $SummaryLines) {
        Write-Host $Line
    }
    Write-Host "Summary: $Summary"
    Write-Host "=============================================================="

    exit $PytestExit
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
