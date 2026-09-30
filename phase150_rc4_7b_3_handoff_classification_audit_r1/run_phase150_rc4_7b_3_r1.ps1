$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7B-3 Handoff Classification Audit R1"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$repo = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$output = Join-Path $package "rc4_7b_3_output.txt"

$env:PYTHONPATH = $repo
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    (Join-Path $package "audit_phase150_rc4_7b_2_support.py") `
    (Join-Path $package "audit_phase150_rc4_7b_3.py")

  Write-Host ""
  Write-Host "B. Running RC4-7B-3 classification audit..."
  python `
    (Join-Path $package "audit_phase150_rc4_7b_3.py") |
    Tee-Object -FilePath $output

  Write-Host ""
  Write-Host "C. Focused existing transition / Argument regressions..."
  pytest -q `
    tests/test_phase143_53a_narrative_transitions.py `
    tests/test_phase143_57a_step_calculation_chain.py `
    tests/test_phase143_46_multi_argument_narrative_assembler.py

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-7B-3 R1 audit finished."
  Write-Host "Production changes: none."
  Write-Host "Output:"
  Write-Host $output
  Write-Host "Do not run the whole repository test suite in this audit."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
