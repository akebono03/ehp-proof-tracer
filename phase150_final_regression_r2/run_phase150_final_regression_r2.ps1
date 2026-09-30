$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Final Regression R2"
Write-Host "Full regression + performance baseline"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

$Output = ".\phase150_final_regression_r2.txt"
$Summary = ".\phase150_final_regression_r2_summary.txt"

try {
    Write-Host ""
    Write-Host "A. Full pytest regression with duration reporting..."
    $Started = Get-Date

    python -m pytest tests -q `
      --durations=50 `
      --durations-min=1.0 `
      2>&1 |
      Tee-Object -FilePath $Output

    $PytestExit = $LASTEXITCODE
    $Elapsed = (Get-Date) - $Started

    $Lines = @(
      "Phase 150 Final Regression R2",
      "========================================",
      ("pytest exit code: {0}" -f $PytestExit),
      ("elapsed seconds: {0:N2}" -f $Elapsed.TotalSeconds),
      ("elapsed: {0}" -f $Elapsed),
      ("output: {0}" -f $Output),
      "Performance Repair R1 included: yes",
      "Full regression executed: yes"
    )

    if ($PytestExit -eq 0) {
      $Lines += "Phase 150 regression status: PASS"
      $Lines += "Next action: Phase 150 documentation/closure"
    }
    else {
      $Lines += "Phase 150 regression status: FAIL"
      $Lines += "Next action: inspect failures; do not finalize documentation"
    }

    $Lines | Set-Content -Path $Summary -Encoding UTF8

    Write-Host ""
    Write-Host "=============================================================="
    Get-Content $Summary
    Write-Host "=============================================================="
    Write-Host "Upload:"
    Write-Host "  .\phase150_final_regression_r2_summary.txt"
    Write-Host "  .\phase150_final_regression_r2.txt"
    Write-Host "=============================================================="

    exit $PytestExit
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
