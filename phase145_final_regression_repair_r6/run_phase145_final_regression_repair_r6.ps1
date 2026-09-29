$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Final Regression Repair R6"
Write-Host "Add explicit tests package marker"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal package-marker repair..."
    python ".\phase145_final_regression_repair_r6\apply_phase145_final_regression_repair_r6.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Final Regression Repair R6 apply failed."
    }

    Write-Host ""
    Write-Host "B. Direct import preflight..."
    python -c "import tests.test_phase143_19_method_evidence; import tests.test_phase75_515_pi15_8_final_group; import tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation; print('Direct canonical helper imports: PASS')"
    if ($LASTEXITCODE -ne 0) {
        throw "Direct canonical helper import preflight failed."
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
    Write-Host "Phase 145 Final Regression Repair R6 focused gate: PASS"
    Write-Host "Repository-wide pytest execution: NOT RUN"
    Write-Host "Next and final Phase 145 gate: python -m pytest tests -q"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
