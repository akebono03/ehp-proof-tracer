$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 152 - Generic Defect Classification"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$PSScriptRoot\audit_phase152.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Syntax preflight failed."
    }

    Write-Host ""
    Write-Host "B. Focused current-pipeline tests..."
    python -m pytest -q `
        "tests/test_phase144_6_r5_43_1.py" `
        "tests/test_phase150_rc4_4_reasons.py" `
        "tests/test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Focused tests failed."
    }

    Write-Host ""
    Write-Host "C. Reproduce Phase 151 baseline and classify observed defects..."
    python "$PSScriptRoot\audit_phase152.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 152 classification audit failed."
    }

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 152 Generic Defect Classification: PASS"
    Write-Host "Output: .\phase152_generic_defect_classification\audit_output\"
    Write-Host "Production changes: none"
    Write-Host "Existing test changes: none"
    Write-Host "Full historical regression: not run"
    Write-Host "Next boundary: choose one confirmed defect category for Phase 153"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
