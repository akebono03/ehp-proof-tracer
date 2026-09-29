$ErrorActionPreference = "Stop"
python ".\phase143_75ap_r17_audit\audit.py" |
  Tee-Object -FilePath ".\phase143_75ap_r17_audit\output.txt"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""
Write-Host "Phase 143-75AP R17 audit complete."
Write-Host "Upload .\phase143_75ap_r17_audit\output.txt"
