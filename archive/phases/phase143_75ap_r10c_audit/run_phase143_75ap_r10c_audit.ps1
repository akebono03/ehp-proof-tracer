$ErrorActionPreference = "Stop"

try {
  python ".\phase143_75ap_r10c_audit\audit_phase143_75ap_r10c.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 143-75AP R10C call-site audit finished."
  Write-Host "=============================================================="
  Write-Host "Read-only audit. No files were modified."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
