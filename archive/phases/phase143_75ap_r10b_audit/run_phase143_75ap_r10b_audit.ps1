$ErrorActionPreference = "Stop"

$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ap_r10b_audit\audit_phase143_75ap_r10b.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 143-75AP R10B recursive audit finished."
  Write-Host "=============================================================="
  Write-Host "Read-only audit. No files were modified."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
