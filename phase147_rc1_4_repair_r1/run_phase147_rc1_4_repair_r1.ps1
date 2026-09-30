$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 147 RC1-4 Ownership Integration Audit Repair R1"
Write-Host "Runner-only repair: repository root PYTHONPATH"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$PreviousPythonPath = $env:PYTHONPATH
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase147_rc1_4_ownership_integration_audit\audit_phase147_rc1_4.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "B. RC1-4 integration audit..."
  python `
    ".\phase147_rc1_4_ownership_integration_audit\audit_phase147_rc1_4.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "C. RC1-3 ownership regression..."
  python -m pytest `
    ".\tests\test_phase147_rc1_argument_method_ownership.py" `
    ".\tests\test_phase143_34_argument_header_method.py" `
    -q
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 147 RC1-4 audit runner: PASS"
  Write-Host "Production changes: none"
  Write-Host "Repository-wide tests intentionally not run."
  Write-Host "=============================================================="
}
finally {
  if ($null -eq $PreviousPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  }
  else {
    $env:PYTHONPATH = $PreviousPythonPath
  }

  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
