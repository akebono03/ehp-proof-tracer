$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here
$Output = Join-Path $Here "r25_30_output.txt"
Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-30 Group-Structure / Definition Entry-Branch Ownership Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"
  Write-Host "`nA. Syntax preflight..."
  python -m py_compile ".\phase144_6_r25_30_group_structure_definition_entry_branch_ownership_audit\audit_phase144_6_r25_30.py" ".\phase144_6_r25_30_group_structure_definition_entry_branch_ownership_audit\test_phase144_6_r25_30.py"
  if ($LASTEXITCODE -ne 0) { throw "R25-30 syntax preflight failed." }
  Write-Host "`nB. Focused audit-contract tests..."
  pytest -q ".\phase144_6_r25_30_group_structure_definition_entry_branch_ownership_audit\test_phase144_6_r25_30.py"
  if ($LASTEXITCODE -ne 0) { throw "R25-30 focused audit-contract tests failed." }
  Write-Host "`nC. Existing argument local-body regressions..."
  pytest -q ".\tests\test_phase143_41_argument_local_body.py"
  if ($LASTEXITCODE -ne 0) { throw "R25-30 existing local-body regressions failed." }
  Write-Host "`nD. Entry-branch ownership audit..."
  python ".\phase144_6_r25_30_group_structure_definition_entry_branch_ownership_audit\audit_phase144_6_r25_30.py" | Tee-Object -FilePath $Output
  if ($LASTEXITCODE -ne 0) { throw "R25-30 audit failed." }
  Write-Host "`n=============================================================="
  Write-Host "R25-30 diagnosis completed."
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
