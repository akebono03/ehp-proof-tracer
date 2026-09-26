$ErrorActionPreference = "Stop"
python ".\phase143_75ap_r16_import_audit\audit.py" |
  Tee-Object -FilePath ".\phase143_75ap_r16_import_audit\output.txt"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""
Write-Host "R16 import/display_steps audit complete."
Write-Host "Upload .\phase143_75ap_r16_import_audit\output.txt"
