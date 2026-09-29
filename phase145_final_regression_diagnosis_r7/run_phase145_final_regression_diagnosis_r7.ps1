$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Final Regression Diagnosis R7"
Write-Host "Mixed canonical test import-style audit"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
    python ".\phase145_final_regression_diagnosis_r7\diagnose_phase145_final_regression_r7.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 145 Final Regression Diagnosis R7 failed."
    }

    Write-Host ""
    Write-Host "Git status for package marker only:"
    git status --short -- tests/__init__.py

    Write-Host ""
    Write-Host "No repository-wide pytest was run."
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
