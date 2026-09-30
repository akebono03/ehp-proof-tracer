$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 151-3 - Cross-cutting Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$PSScriptRoot\audit_phase151_3.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Syntax preflight failed."
    }

    Write-Host ""
    Write-Host "B. Focused generic/block/reason tests..."
    python -m pytest -q `
        "tests/test_phase144_6_r5_43_1.py" `
        "tests/test_phase150_rc4_4_reasons.py" `
        "tests/test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Focused tests failed."
    }

    Write-Host ""
    Write-Host "C. Reproducing Phase 151-2 baseline and running cross-cutting audit..."
    python "$PSScriptRoot\audit_phase151_3.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Cross-cutting audit failed."
    }

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 151-3 Cross-cutting Audit: PASS"
    Write-Host "Output: .\phase151_3_cross_cutting_audit\audit_output\"
    Write-Host "Production changes: none"
    Write-Host "Existing test changes: none"
    Write-Host "Full historical regression: not run"
    Write-Host "Next boundary: Phase 152 defect classification only"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
