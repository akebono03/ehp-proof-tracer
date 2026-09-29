$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python ".\phase143_75ap_r14_completion_audit\audit_phase143_75ap_r14_completion.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "Do not run the full pytest suite from this package."
  Write-Host "If this audit passes, the next step is the one final Phase 143 regression."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
