$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 149 RC3-5 Repair R1"
Write-Host "Documentation closure only"
Write-Host "Repository-wide regression is NOT repeated"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  $originalDir = ".\phase149_rc3_5_final_regression_documentation_closure"
  $repairDir = ".\phase149_rc3_5_repair_r1"
  $summaryPath = Join-Path $originalDir "repository_regression_summary.txt"

  Write-Host ""
  Write-Host "A. Verifying successful Phase-final regression evidence..."
  if (-not (Test-Path $summaryPath)) {
    throw "Missing repository_regression_summary.txt from the successful RC3-5 run."
  }

  $summary = (Get-Content $summaryPath -Raw).Trim()
  if ($summary -notmatch '^\d+ passed in ') {
    throw "Unexpected repository regression summary: $summary"
  }
  Write-Host $summary

  Write-Host ""
  Write-Host "B. Syntax preflight for repaired documentation scripts..."
  python -m py_compile `
    "$repairDir\apply_phase149_rc3_5_documentation.py" `
    "$repairDir\verify_phase149_rc3_5_documentation.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Python syntax preflight failed."
  }

  Write-Host ""
  Write-Host "C. Copying measured regression summary into repair package..."
  Copy-Item `
    $summaryPath `
    "$repairDir\repository_regression_summary.txt" `
    -Force

  Write-Host ""
  Write-Host "D. Applying Phase 149 documentation closure..."
  python "$repairDir\apply_phase149_rc3_5_documentation.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Documentation application failed."
  }

  Write-Host ""
  Write-Host "E. Verifying documentation closure..."
  python "$repairDir\verify_phase149_rc3_5_documentation.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Documentation verification failed."
  }

  Write-Host ""
  Write-Host "F. Git diff summary..."
  git diff --stat -- `
    README.md `
    docs/design.md `
    docs/development_log.md `
    docs/roadmap.md `
    docs/proof_records.md `
    toda_group_proof_narrative_argument_body_renderer.py `
    tests/test_phase149_rc3_3_minimal_ordering.py `
    tests/test_phase149_rc3_4_cross_group_ordering.py
  if ($LASTEXITCODE -ne 0) {
    throw "git diff summary failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 149 RC3-5 Repair R1 completed successfully."
  Write-Host "Phase 149 / RC3 is closed."
  Write-Host "Repository-wide regression reused: $summary"
  Write-Host "Next boundary: Phase 150 / RC4 Generic provenance / reason prose."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
