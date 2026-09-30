$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7B Argument-Flow Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$AuditDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile "$AuditDir\audit_phase150_rc4_7b_argument_flow.py"

    Write-Host ""
    Write-Host "B. Argument-flow audit..."
    python "$AuditDir\audit_phase150_rc4_7b_argument_flow.py" |
        Tee-Object -FilePath "$AuditDir\rc4_7b_argument_flow_output.txt"

    Write-Host ""
    Write-Host "C. Focused existing regression..."
    python -m pytest -q `
        tests/test_phase143_7_narrative_arguments.py `
        tests/test_phase143_41_argument_local_body.py `
        tests/test_phase143_46_multi_argument_narrative_assembler.py `
        tests/test_phase147_rc1_argument_method_ownership.py `
        tests/test_phase150_rc4_7a_cross_group_reference_normalization.py

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "RC4-7B argument-flow audit completed."
    Write-Host "Production changes: none"
    Write-Host "Existing test changes: none"
    Write-Host "Repository-wide tests were intentionally not run."
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
