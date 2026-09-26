$ErrorActionPreference = "Stop"
python ".\phase143_75ap_r17_completion_audit_r2\audit_current_entrypoint.py" |
  Tee-Object -FilePath ".\phase143_75ap_r17_completion_audit_r2\output.txt"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""
Write-Host "Current Phase143 Narrative entrypoint audit complete."
Write-Host "Upload .\phase143_75ap_r17_completion_audit_r2\output.txt"
