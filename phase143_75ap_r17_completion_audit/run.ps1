$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Get-Location).Path
try {
  python ".\phase143_75ap_r17_completion_audit\run_existing_completion_audit.py" |
    Tee-Object -FilePath ".\phase143_75ap_r17_completion_audit\output.txt"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "R17 completion audit finished."
  Write-Host "Upload .\phase143_75ap_r17_completion_audit\output.txt"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
