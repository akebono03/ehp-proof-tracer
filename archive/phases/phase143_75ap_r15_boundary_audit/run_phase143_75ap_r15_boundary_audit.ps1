$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path
try {
  python ".\phase143_75ap_r15_boundary_audit\audit_phase143_75ap_r15_boundary.py" |
    Tee-Object -FilePath ".\phase143_75ap_r15_boundary_audit\phase143_75ap_r15_boundary_output.txt"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Write-Host ""
  Write-Host "Phase 143-75AP R15 boundary audit complete."
  Write-Host "Upload phase143_75ap_r15_boundary_output.txt"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
