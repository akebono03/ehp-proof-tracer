$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 149 RC3-1 Narrative Ordering Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$env:PYTHONPATH = $repoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Syntax preflight..."
    python -m py_compile `
      ".\phase149_rc3_1_ordering_audit\audit_phase149_rc3_1.py"

    Write-Host ""
    Write-Host "B. Running pi_6^3 ordering audit..."
    python `
      ".\phase149_rc3_1_ordering_audit\audit_phase149_rc3_1.py" |
      Tee-Object `
        -FilePath ".\phase149_rc3_1_ordering_audit\rc3_1_output.txt"

    Write-Host ""
    Write-Host "C. Focused existing RC2 tests..."
    pytest -q `
      ".\tests\test_phase148_rc2_4_cross_group_audit.py" `
      ".\tests\test_phase148_rc2_4_post_repair_six_group.py"

    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "RC3-1 audit completed."
    Write-Host "No production files were changed."
    Write-Host "Do not run repository-wide tests in RC3-1."
    Write-Host "Please paste rc3_1_output.txt and pytest output into ChatGPT."
    Write-Host "=============================================================="
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
