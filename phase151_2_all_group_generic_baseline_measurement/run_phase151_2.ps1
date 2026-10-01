$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 151-2 - All-Group Generic Baseline Measurement"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="
$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"
try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$PSScriptRoot\audit_phase151_2.py"
    if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

    Write-Host ""
    Write-Host "B. Focused reason/generic renderer tests..."
    python -m pytest -q `
        "tests/test_phase150_rc4_4_reasons.py" `
        "tests/test_phase144_6_r5_43_1.py" `
        "tests/test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py"
    if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }

    Write-Host ""
    Write-Host "C. Measuring all 112 groups..."
    python "$PSScriptRoot\audit_phase151_2.py"
    if ($LASTEXITCODE -ne 0) { throw "Baseline measurement completed with failures." }

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "Phase 151-2 baseline measurement: PASS"
    Write-Host "Output: .\phase151_2_all_group_generic_baseline_measurement\audit_output\"
    Write-Host "Production changes: none"
    Write-Host "Full historical regression: not run"
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
