$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Final Regression Repair R3"
Write-Host "Transitive canonical test dependency restoration"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Restoring archived canonical dependencies to fixed point..."
    python ".\phase145_final_regression_repair_r3\apply_phase145_final_regression_repair_r3.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Final Regression Repair R3 apply failed."
    }

    Write-Host ""
    Write-Host "B. Syntax preflight for canonical test tree..."
    $canonicalTests = Get-ChildItem ".\tests" -Filter "*.py" -File
    foreach ($file in $canonicalTests) {
        python -m py_compile $file.FullName
        if ($LASTEXITCODE -ne 0) {
            throw "Syntax preflight failed: $($file.FullName)"
        }
    }

    Write-Host ""
    Write-Host "C. Canonical test collection only..."
    python -m pytest tests --collect-only -q
    if ($LASTEXITCODE -ne 0) {
        throw "Canonical test collection failed."
    }

    Write-Host ""
    Write-Host "D. Phase 145 focused regression..."
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
    Write-Host "Phase 145 Final Regression Repair R3 focused gate: PASS"
    Write-Host "Repository-wide pytest execution: NOT RUN"
    Write-Host "Next gate after PASS: one final python -m pytest tests -q"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
