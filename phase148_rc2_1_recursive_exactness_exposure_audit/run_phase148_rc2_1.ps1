$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-1 Recursive Exactness Evidence Exposure Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    "$PackageDir\audit_phase148_rc2_1.py" `
    "$PackageDir\test_phase148_rc2_1.py"

  Write-Host ""
  Write-Host "B. Focused boundary tests..."
  pytest -q `
    "$PackageDir\test_phase148_rc2_1.py" `
    "tests\test_phase147_rc1_argument_method_ownership.py" `
    "tests\test_phase143_38_exactness_display_contributions.py" `
    "tests\test_phase143_39_exactness_contribution_ownership.py"

  Write-Host ""
  Write-Host "C. Exposure audit..."
  python "$PackageDir\audit_phase148_rc2_1.py" |
    Tee-Object -FilePath "$PackageDir\rc2_1_output.txt"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 148 RC2-1 audit package: PASS"
  Write-Host "No repository-wide pytest in RC2-1."
  Write-Host "Next boundary: RC2-2 general exposure-rule design."
  Write-Host "RC3 ordering remains untouched."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
