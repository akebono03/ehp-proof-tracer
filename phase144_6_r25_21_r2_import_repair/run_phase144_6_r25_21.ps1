$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Here

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-21 Presentation Rules Audit"
Write-Host "AUDIT ONLY - production changes: none"
Write-Host "=============================================================="
Write-Host ""

Push-Location $Repo
try {
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTHONIOENCODING = "utf-8"

  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase144_6_r25_21_presentation_rules_audit\audit_phase144_6_r25_21.py" `
    ".\phase144_6_r25_21_presentation_rules_audit\test_phase144_6_r25_21.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-21 syntax preflight failed."
  }
  Write-Host ""

  Write-Host "B. R25-21 focused specification checks..."
  pytest -q `
    ".\phase144_6_r25_21_presentation_rules_audit\test_phase144_6_r25_21.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-21 focused checks failed."
  }
  Write-Host ""

  Write-Host "C. Generating legacy-vs-six-group presentation audit..."
  python `
    ".\phase144_6_r25_21_presentation_rules_audit\audit_phase144_6_r25_21.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R25-21 audit failed."
  }
  Write-Host ""

  Write-Host "=============================================================="
  Write-Host "R25-21 completed."
  Write-Host "Inspect:"
  Write-Host ".\phase144_6_r25_21_presentation_rules_audit\output\r25_21_presentation_rules_audit.md"
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  Pop-Location
}
