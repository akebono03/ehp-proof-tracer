$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Final Regression 9-Failure Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Inspecting exact local contracts..."
    python "$ScriptRoot\audit_phase150_final_regression_9_failures.py" |
      Tee-Object -FilePath "$ScriptRoot\phase150_9_failure_audit_output.txt"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Re-running only the failing parametrized contracts..."
    python -m pytest `
      "tests/test_phase148_rc2_4_repair_r5.py::test_phase148_rc2_4_repair_r5_audit_reproduces_one_visible_raw_exactness" `
      "tests/test_phase148_rc2_4_repair_r5_r2.py::test_phase148_rc2_4_repair_r5_r2_remaining_exactness_phrase_is_distinct_from_raw_window" `
      "tests/test_phase150_rc4_5_visible_reasons.py::test_phase150_rc4_5_visible_reason_count_matches_typed_reason_count" `
      -q `
      --tb=line |
      Tee-Object -FilePath "$ScriptRoot\phase150_9_failure_focused_pytest.txt"

    $FocusedExitCode = $LASTEXITCODE
    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Focused pytest exit code: $FocusedExitCode"
    Write-Host "A nonzero code is expected while the 9 contracts remain unresolved."
    Write-Host "Full regression: NOT run"
    Write-Host "=============================================================="
    exit 0
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
