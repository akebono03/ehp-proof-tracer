$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 151-1 — All-Group Generic Baseline Feasibility Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile `
        "$PSScriptRoot\audit_phase151_1.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Syntax preflight failed."
    }

    Write-Host ""
    Write-Host "B. Focused existing tests..."
    python -m pytest -q `
        "tests/test_phase144_6_public_route_cutover.py" `
        "tests/test_phase144_6_r5_43_1.py" `
        "tests/test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Focused existing tests failed."
    }

    Write-Host ""
    Write-Host "C. All-group generic feasibility audit..."
    python "$PSScriptRoot\audit_phase151_1.py"
    if ($LASTEXITCODE -ne 0) {
        throw "All-group generic feasibility audit did not pass."
    }

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 151-1 feasibility audit: PASS"
    Write-Host "No production files changed."
    Write-Host "No existing tests changed."
    Write-Host "Full historical regression was not run."
    Write-Host "Next boundary: Phase 151-2 baseline measurement only."
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
