$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Final Regression Repair R2"
Write-Host "Restore canonical test dependencies misclassified as historical"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal dependency restoration..."
    python ".\phase145_final_regression_repair_r2\apply_phase145_final_regression_repair_r2.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Final Regression Repair R2 apply failed."
    }

    Write-Host ""
    Write-Host "B. Python syntax preflight for restored canonical dependencies..."
    $restored = git diff --cached --name-status |
        ForEach-Object {
            $parts = $_ -split "`t"
            if ($parts.Count -ge 3 -and $parts[0] -match "^R") {
                $parts[2]
            }
        } |
        Where-Object {
            ($_ -like "tests/*.py") -or
            (($_ -notlike "*/*") -and ($_ -like "audit_phase*.py"))
        }

    foreach ($file in $restored) {
        python -m py_compile $file
        if ($LASTEXITCODE -ne 0) {
            throw "Syntax preflight failed: $file"
        }
    }

    Write-Host ""
    Write-Host "C. Canonical test collection only..."
    python -m pytest tests --collect-only -q
    if ($LASTEXITCODE -ne 0) {
        throw "Canonical test collection failed."
    }

    Write-Host ""
    Write-Host "D. Phase 145 default focused regression..."
    python -m pytest -q `
      ".\tests\test_phase145_group_proof_defaults.py" `
      ".\tests\test_phase132_7_group_proof_cli_modes.py" `
      ".\tests\test_phase131_4_group_result_proof_replay_cli.py" `
      ".\tests\test_phase132_9_web_group_proof_modes.py" `
      ".\tests\test_phase131_5_web_group_proof.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145 focused regression failed."
    }

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 145 Final Regression Repair R2 focused gate: PASS"
    Write-Host "Repository-wide pytest execution: NOT RUN"
    Write-Host "Next gate after PASS: one final python -m pytest tests -q"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
