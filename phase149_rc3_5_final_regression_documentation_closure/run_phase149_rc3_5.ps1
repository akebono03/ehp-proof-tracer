$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 149 RC3-5 Final Regression / Documentation Closure"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Verifying Phase 149 focused regression..."
  pytest -q `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py" `
    ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
    ".\tests\test_phase148_rc2_4_cross_group_audit.py" `
    ".\tests\test_phase148_rc2_4_post_repair_six_group.py"

  Write-Host ""
  Write-Host "B. Running Phase-final repository-wide regression..."
  $output = python -m pytest tests -q 2>&1
  $exitCode = $LASTEXITCODE
  $output | Tee-Object `
    -FilePath ".\phase149_rc3_5_final_regression_documentation_closure\repository_regression_output.txt"

  if ($exitCode -ne 0) {
    throw "Repository-wide regression failed. Documentation closure was NOT applied."
  }

  $summaryLine = (
    $output |
    Select-String -Pattern "passed.*in " |
    Select-Object -Last 1
  ).Line

  if (-not $summaryLine) {
    throw "Could not extract pytest summary. Documentation closure was NOT applied."
  }

  Set-Content `
    -Path ".\phase149_rc3_5_final_regression_documentation_closure\repository_regression_summary.txt" `
    -Value $summaryLine `
    -Encoding UTF8

  Write-Host ""
  Write-Host "Repository-wide regression summary:"
  Write-Host $summaryLine

  Write-Host ""
  Write-Host "C. Applying Phase 149 documentation closure..."
  python `
    ".\phase149_rc3_5_final_regression_documentation_closure\apply_phase149_rc3_5_documentation.py"

  Write-Host ""
  Write-Host "D. Verifying documentation markers and language boundary..."
  python `
    ".\phase149_rc3_5_final_regression_documentation_closure\verify_phase149_rc3_5_documentation.py"

  Write-Host ""
  Write-Host "E. Git diff summary..."
  git diff --stat -- `
    README.md `
    docs/design.md `
    docs/development_log.md `
    docs/roadmap.md `
    docs/proof_records.md `
    toda_group_proof_narrative_argument_body_renderer.py `
    tests/test_phase149_rc3_3_minimal_ordering.py `
    tests/test_phase149_rc3_4_cross_group_ordering.py

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 149 RC3-5 completed."
  Write-Host "Phase 149 / RC3 is closed if all steps above passed."
  Write-Host "Next boundary: Phase 150 / RC4 Generic provenance / reason prose."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
