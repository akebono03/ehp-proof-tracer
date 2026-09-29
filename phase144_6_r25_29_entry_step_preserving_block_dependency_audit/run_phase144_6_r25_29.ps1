$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here
$Output = Join-Path $Here "r25_29_output.txt"
Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-29 Entry-Step-Preserving Block Dependency Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"
  Write-Host "`nA. Syntax preflight..."
  python -m py_compile ".\phase144_6_r25_29_entry_step_preserving_block_dependency_audit\audit_phase144_6_r25_29.py" ".\phase144_6_r25_29_entry_step_preserving_block_dependency_audit\test_phase144_6_r25_29.py"
  if ($LASTEXITCODE -ne 0) { throw "R25-29 syntax preflight failed." }
  Write-Host "`nB. Focused simulation-contract tests..."
  pytest -q ".\phase144_6_r25_29_entry_step_preserving_block_dependency_audit\test_phase144_6_r25_29.py"
  if ($LASTEXITCODE -ne 0) { throw "R25-29 focused simulation-contract tests failed." }
  Write-Host "`nC. Existing argument local-body regressions..."
  pytest -q ".\tests\test_phase143_41_argument_local_body.py"
  if ($LASTEXITCODE -ne 0) { throw "R25-29 existing local-body regressions failed." }
  Write-Host "`nD. Six-group entry-step-preserving simulation..."
  python ".\phase144_6_r25_29_entry_step_preserving_block_dependency_audit\audit_phase144_6_r25_29.py" | Tee-Object -FilePath $Output
  if ($LASTEXITCODE -ne 0) { throw "R25-29 simulation audit failed." }
  Write-Host "`n=============================================================="
  Write-Host "R25-29 diagnosis completed."
  Write-Host "Output: $Output"
  Write-Host "No production files were changed."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
