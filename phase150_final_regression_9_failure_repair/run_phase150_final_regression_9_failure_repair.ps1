$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Final Regression 9-Failure Repair"
Write-Host "Production changes: none"
Write-Host "Changed tests: 3 files"
Write-Host "Documentation changes: none"
Write-Host "Full regression: NOT run"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal test-contract repair..."
    python "$ScriptRoot\apply_phase150_final_regression_9_failure_repair.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host ""
    Write-Host "B. Syntax preflight..."
    python -m py_compile `
      ".\tests\test_phase148_rc2_4_repair_r5.py" `
      ".\tests\test_phase148_rc2_4_repair_r5_r2.py" `
      ".\tests\test_phase150_rc4_5_visible_reasons.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "Syntax preflight: PASS"

    Write-Host ""
    Write-Host "C. Focused regression for the repaired contracts..."
    python -m pytest `
      tests/test_phase148_rc2_4_repair_r5.py `
      tests/test_phase148_rc2_4_repair_r5_r2.py `
      tests/test_phase150_rc4_5_visible_reasons.py `
      -q `
      --tb=line `
      --durations=20 `
      --durations-min=0.0
    $ExitCode = $LASTEXITCODE

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Focused pytest exit code: $ExitCode"
    Write-Host "Completion condition: all focused tests PASS"
    Write-Host "Full regression: NOT run"
    Write-Host "=============================================================="
    exit $ExitCode
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
