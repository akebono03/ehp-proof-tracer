$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Final Regression Repair R8"
Write-Host "Mixed canonical test import compatibility"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Applying minimal compatibility repair..."
    python ".\phase145_final_regression_repair_r8\apply_phase145_final_regression_repair_r8.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145 Final Regression Repair R8 apply failed."
    }

    Write-Host ""
    Write-Host "B. Syntax preflight..."
    python -m py_compile ".\tests\conftest.py"
    if ($LASTEXITCODE -ne 0) {
        throw "tests/conftest.py syntax preflight failed."
    }

    Write-Host ""
    Write-Host "C. Pytest-context mixed-import preflight..."
    python -m pytest --collect-only -q `
      ".\tests\test_phase143_22_exactness_components.py" `
      ".\tests\test_phase143_59a_group_structure_semantic_key.py" `
      ".\tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Mixed-import pytest-context preflight failed."
    }

    Write-Host ""
    Write-Host "D. Canonical test collection only..."
    python -m pytest tests --collect-only -q
    if ($LASTEXITCODE -ne 0) {
        throw "Canonical test collection failed."
    }

    Write-Host ""
    Write-Host "E. Phase 145 focused regression..."
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
    Write-Host "F. Relevant git status..."
    git status --short -- tests/__init__.py tests/conftest.py

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 145 Final Regression Repair R8 focused gate: PASS"
    Write-Host "Repository-wide pytest execution: NOT RUN"
    Write-Host "Final Phase 145 gate after this PASS:"
    Write-Host "  python -m pytest tests -q"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
